import logging
import zipfile

from six.moves.urllib.parse import urlencode, urljoin

import os
import re
import requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import join, abspath
from shutil import rmtree
from subfind.cmd import run_cmd
from subfind.exception import SubtitleFileBroken, HTTPConnectionError, ReleaseNotMatchError, MovieNotFound
from subfind.model import Subtitle
from subfind.movie.alice import MovieScoringAlice
from subfind.movie_parser import parse_release_name
from subfind.provider import BaseProvider
from subfind.release import ReleaseMatchingChecker
from subfind.release.alice import ReleaseScoringAlice
from subfind.scenario import BaseScenarioFactory, Scenario1
from subfind.utils.process import which
from subfind.utils.subtitle import get_subtitle_ext
from subfind_provider_subscene.language import get_full_lang, get_short_lang
from tempfile import mkdtemp

SUBSCENE_SEARCH_URL = "https://subscene.com/subtitles/title?%s"
SUBSCENE_RELEASE_SEARCH_URL = "https://subscene.com/subtitles/release?%s"


class SubsceneFactory(BaseScenarioFactory):
    def get_scenario(self):
        release_scoring = ReleaseScoringAlice()
        provider = SubsceneProvider()

        return Scenario1(release_scoring, provider)


class SubsceneProvider(BaseProvider):
    def __init__(self):
        self.session = requests.Session()

        self.movie_title_year_pattern = re.compile('^(.*)(\s+\((\d+)\))$')
        self.sub_extensions = ['srt', 'sub', 'ass']
        self.logger = logging.getLogger(self.__class__.__name__)

        self.movie_score = MovieScoringAlice()

        # Validate if unrar exists
        tmp = which('unrar')
        if tmp is None:
            self.logger.warning('Could not find unrar command. Some subtitle maybe could not extract')
            self.has_unrar = False
        else:
            self.has_unrar = True
        # print(tmp)

    def search_movie(self, release_name, langs):
        release_matching_checker = ReleaseMatchingChecker(release_name)

        movies = self.get_all_movies(release_name=release_name, release_matching_checker=release_matching_checker)

        if not movies:
            return movies

        movie = movies[0]

        return self._get_movie_release(release_matching_checker, movie, langs)

    def get_all_movies(self, release_name, release_matching_checker=None):
        """
        Search all movies match with this releases
        :param release_matching_checker:
        :type release_matching_checker:
        :param release_name:
        :type release_name:
        :return:
        :rtype:
        """
        if release_matching_checker is None:
            release_matching_checker = ReleaseMatchingChecker(release_name)

        query = release_matching_checker.info['title_query']
        base_url = (SUBSCENE_SEARCH_URL % urlencode({'q': query}))

        r = self.session.get(base_url)

        if not r.ok:
            # print('not ok')
            return []

        if '/release?q=' in r.url:
            # Response is redirect to release search page
            # So, we return a mock movie
            return [
                {
                    'display_title': query,
                    'title': query,
                    'url': r.url,
                    'mock': True
                }
            ]

        soup = BeautifulSoup(r.content, 'html.parser')

        nodes = soup.find_all('div', attrs={'class': 'title'})

        movie_nodes = []
        for node in nodes:
            a_nodes = node.find_all('a')
            if not a_nodes:
                continue

            found = False
            for a_node in a_nodes:
                if '/subtitles/' in a_node.attrs['href']:
                    found = True
                    break

            if found:
                movie_nodes.append(a_node)

        movies = []
        processed_urls = set()
        for node in movie_nodes:
            url = node.attrs['href']
            if url.startswith('/subtitles/release?'):
                continue

            movie_url = urljoin(base_url, url)
            if movie_url in processed_urls:
                continue

            processed_urls.add(movie_url)

            movie_display_title = node.text.strip()

            # The movie title in url is better than the movie_display_title
            # E.g.: https://subscene.com/subtitles/dragon-blade-2015
            # movie_display_title = 'Dragon Blade (Tian jiang xiong shi)'
            # movie_title = 'dragon blade'
            movie_title = self._get_movie_title_from_url(movie_url)

            m = self.movie_title_year_pattern.search(movie_display_title)
            movie_year = -1
            if m:
                movie_display_title = m.group(1).strip()
                if m.group(2):
                    movie_year = int(m.group(3).strip())

            movies.append({
                'display_title': movie_display_title,
                'title': movie_title,
                'year': movie_year,
                'url': movie_url
            })

        if not movies:
            # No movie found
            return movies

        # Sort movie base on release info, the best match movie should be first
        self.movie_score.sort(release_matching_checker.info, movies)

        filtered_movies = self.movie_score.get_match(release_matching_checker.info, movies)

        return filtered_movies

    def _get_movie_release(self, release_matching_checker, movie, langs):
        base_url = movie['url']
        r = self.session.get(base_url)

        if not r.ok:
            raise HTTPConnectionError(base_url, r.status_code, r.content)

        soup = BeautifulSoup(r.content, 'html.parser')
        nodes = soup.find_all('td')
        release_nodes = []
        for node in nodes:
            a_nodes = list(filter(lambda a: '/subtitles/' in a.attrs['href'], node.find_all('a')))

            if not a_nodes:
                continue

            a_node = a_nodes[0]

            release_nodes.append(a_node)

        ret = {}
        if not release_nodes:
            return ret

        release_not_match = {}

        for release_node in release_nodes:
            release_lang = release_node.find('span').text.strip()

            release_lang = get_short_lang(release_lang)

            if release_lang not in langs:
                continue

            if release_lang not in ret:
                ret[release_lang] = []

            item_release_name = release_node.find_all('span')[1].text.strip()

            release_url = urljoin(base_url, release_node.get('href'))

            release = {
                'name': item_release_name,
                'lang': release_lang,
                'url': release_url
            }

            try:
                release_matching_checker.check(item_release_name)
            except ReleaseNotMatchError:
                if release_lang not in release_not_match:
                    release_not_match[release_lang] = []

                release_not_match[release_lang].append(release)
                continue
            except MovieNotFound:
                # Could not parse release name
                # E.g.: https://subscene.com/subtitles/bad-boys-ii/english/129659
                # release_name = `x264-uSk`
                continue

            ret[release_lang].append(release)

        # Try to use not match release if not found match release
        for release_lang in ret:
            if not ret[release_lang]:
                self.logger.debug('Not found match release for %s. Use not match version' % release_lang)
                ret[release_lang] = release_not_match.get(release_lang, [])

        return ret

    def get_movie_subs(self, movie, params, lang):
        movie_url = movie['url']
        # print movie_url
        r = self.session.get(movie_url)
        # print r.content

        m = re.compile('/subtitles/([^/]+)$').search(movie_url)
        movie_slug_name = m.group(1)

        lang_full_name = get_full_lang(lang)

        soup = BeautifulSoup(r.content, 'html.parser')
        href_pattern = "/subtitles/%s/%s/" % (movie_slug_name, lang_full_name)
        nodes = soup.find_all('a')
        a_nodes = []
        for node in nodes:
            if href_pattern in node.get('href'):
                a_nodes.append(node)

        subtitles = []
        for node in a_nodes:
            subtitle_url = node.get('href')
            subtitle_name = node.find_all('span')[1].text.strip()

            subtitles.append({
                'url': urljoin(movie_url, subtitle_url),
                'name': subtitle_name,
            })

        return subtitles

    def get_sub(self, release):
        sub_page_url = release['url']
        r = self.session.get(sub_page_url)
        if not r.ok:
            # print r.content
            raise SubtitleFileBroken(url=sub_page_url, message='Could not download url. Status code: %s' % r.status_code)

        m = re.search('href=\"(/subtitle/download[^\'"]+)"', r.text)
        if not m:
            # print 'Could not find download url'
            raise SubtitleFileBroken(url=sub_page_url, message='Could not find download url from html content')

        sub_download_url = urljoin(sub_page_url, m.group(1))

        tmp_folder = mkdtemp(prefix='subfind-')
        try:
            response = self.session.get(sub_download_url, stream=True)
            if not response.ok:
                # Something went wrong
                # print 'could not download sub file'
                raise SubtitleFileBroken(url=sub_page_url, message='Could not download subtitle content. Status code: %s' % response.status_code)

            file_format = 'zip'
            if 'rar' in response.headers['Content-Type']:
                file_format = 'rar'

            tmp_file = abspath(join(tmp_folder, 'tmp.%s' % file_format))

            with open(tmp_file, 'wb') as handle:
                for block in response.iter_content(1024):
                    handle.write(block)

            if file_format == 'zip':
                try:
                    with open(tmp_file, 'rb') as fh:
                        z = zipfile.ZipFile(fh)
                        num_items = 0
                        for item in z.namelist():
                            num_items += 1
                            for sub_extension in self.sub_extensions:
                                if item.endswith('.%s' % sub_extension):
                                    z.extract(item, tmp_folder)
                                    sub_file = join(tmp_folder, item)

                                    return Subtitle(content=open(sub_file, 'rb').read(), extension=sub_extension)

                        if num_items == 0:
                            raise SubtitleFileBroken(url=sub_page_url, message='Could not find any file in subtitle file')
                except zipfile.BadZipFile:
                    raise SubtitleFileBroken(url=sub_page_url, message='Subtitle file broken')
            elif file_format == 'rar':
                if not self.has_unrar:
                    raise Exception('Could not extract rar because missing unrar command')

                run_cmd('unrar e -inul %s' % tmp_file, cwd=tmp_folder)
                for item in os.listdir(tmp_folder):
                    sub_extension = get_subtitle_ext(item)
                    if not sub_extension:
                        continue

                    sub_file = join(tmp_folder, item)
                    return Subtitle(content=open(sub_file, 'rb').read(), extension=sub_extension)
            else:
                raise Exception('Un-support extract file extension %s' % file_format)

            self.logger.warning('There is no subtitle extension found. Files:')
            for item in listdir(tmp_folder):
                self.logger.warning(item)

            raise SubtitleFileBroken(url=sub_page_url, message='There is no subtitle extension found')
        finally:
            # Remove tmp_folder
            rmtree(tmp_folder)

    def get_releases(self, release_name, langs):
        return self.search_movie(release_name, langs)

    @staticmethod
    def _get_movie_title_from_url(movie_url):
        title_in_url = movie_url[movie_url.rfind('/'):]
        # print(title_in_url)
        info = parse_release_name(title_in_url)
        # print(info)
        return info['title_query']


if __name__ == '__main__':
    print(SubsceneProvider.get_movie_title_from_url('https://subscene.com/subtitles/dragon-blade-2015'))
