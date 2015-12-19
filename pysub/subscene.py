import logging
import os
import re
import urllib
from os import listdir
from os.path import join, exists, abspath, getsize
from shutil import rmtree
from tempfile import mkdtemp
from urlparse import urljoin

import distance
import requests

from pysub.cmd import run_cmd
from pysub.exception import MovieNotFound, SubtitleNotFound, SubtitleFileBroken
from pysub.lang import get_full_lang
from pysub.parser import Parser
from pysub.tokenizer import tokenizer

SUBSCENE_SEARCH_URL = "http://subscene.com/subtitles/title?%s"

subsence_lang_name_lookup = {
    'vi': 'vietnamese'
}


def movie_cmp(a, b):
    if a['d'] < b['d']:
        # smaller distances is better
        return -1
    elif a['d'] > b['d']:
        return 1

    if a['year'] > b['year']:
        # larger year is better
        return -1
    elif a['year'] < b['year']:
        return 1

    return 0


class SubFinder(object):
    def __init__(self, languages, force=False):
        self.force = force
        self.languages = languages

        assert isinstance(languages, list)

        self.movie_extensions = ['mp4', 'mkv']
        self.movie_file_pattern = re.compile('^(.+)\.\w+$')
        self.not_title_tokens = set(['x264', '1080p', '1080', 'hdrip'])
        self.year_pattern = re.compile('^(19\d{2}|201\d)$')
        self.movie_title_year_pattern = re.compile('^(.*)(\s+\((\d+)\))$')

        # Ignore movie file which size < 500MB
        self.min_movie_size = 500 * 1000 * 1000

        self.session = requests.Session()

        self.logger = logging.getLogger(self.__class__.__name__)

    def _search_movies(self, params):
        query = params['movie_title_search_query']
        base_url = (SUBSCENE_SEARCH_URL % urllib.urlencode({'q': query}))

        # print params

        # print base_url

        r = self.session.get(base_url)
        # print r.content

        if not r.ok:
            return []

        parser = Parser(r.content)
        nodes = parser.query('//div[@class="title"]/a[contains(@href, "/subtitles/")]')

        movies = []
        processed_urls = set()
        for node in nodes:
            url = node.get('href')
            # print url
            # continue
            if url.startswith('/subtitles/release?'):
                continue

            movie_url = urljoin(base_url, url)
            if movie_url in processed_urls:
                continue

            processed_urls.add(movie_url)

            movie_title = node.text.strip()
            m = self.movie_title_year_pattern.search(movie_title)
            movie_year = -1
            if m:
                movie_title = m.group(1).strip()
                if m.group(2):
                    movie_year = int(m.group(3).strip())

                    if params.get('year') and movie_year != params.get('year'):
                        # Ignore invalid year movie
                        continue

            movies.append({
                'title': movie_title,
                'year': movie_year,
                'd': distance.levenshtein(query, movie_title.lower()),
                'url': movie_url
            })

        movies.sort(cmp=movie_cmp)

        # pprint(movies)
        # raise SystemExit
        if movies:
            return movies[0]

        return None

    def _get_sub_file(self, sub_page_url):
        r = self.session.get(sub_page_url)
        if not r.ok:
            print r.content
            return None

        m = re.search('href=\"(/subtitle/download[^\'"]+)"', r.content)
        if not m:
            print 'Could not find download url'
            return None

        sub_download_url = urljoin(sub_page_url, m.group(1))
        # print sub_download_url

        # subprocess.call()

        # tmp_folder = 'tmp'
        # if not exists(tmp_folder):
        #     os.makedirs(tmp_folder)
        tmp_folder = mkdtemp(prefix='pysub-')
        try:
            tmp_file = abspath(join(tmp_folder, 'tmp.zip'))

            # run_cmd('rm %s/* -rf' % tmp_folder)

            response = requests.get(sub_download_url, stream=True)
            if not response.ok:
                # Something went wrong
                print 'could not download sub file'
                return None

            with open(tmp_file, 'wb') as handle:
                for block in response.iter_content(1024):
                    handle.write(block)

            self.logger.debug('Unzip tmp file: %s' % tmp_folder)
            run_cmd('unzip -o %s' % tmp_file, silent=True, cwd=tmp_folder)

            self.logger.debug('tmp tmp file: %s' % tmp_folder)
            run_cmd('rm %s' % tmp_file, silent=True, cwd=tmp_folder)

            sub_extensions = ['srt', 'sub', 'ass']
            # print 'hello'
            num_items = 0
            for item in listdir(tmp_folder):
                # print item
                num_items += 1
                for sub_extension in sub_extensions:
                    if item.endswith('.%s' % sub_extension):
                        return open(join(tmp_folder, item)).read()

            # print tmp_folder
            if num_items == 0:
                raise SubtitleFileBroken(url=sub_page_url, message='Could not find any file in subtitle file')

            self.logger.warning('There is no subtitle extension found. Files:')
            for item in listdir(tmp_folder):
                self.logger.warning(item)

            return None
        finally:
            # Remove tmp_folder
            rmtree(tmp_folder)

    def _get_movie_subs(self, movie, params, lang):
        movie_url = movie['url']
        # print movie_url
        r = self.session.get(movie_url)
        # print r.content

        m = re.compile('/subtitles/([^/]+)$').search(movie_url)
        movie_slug_name = m.group(1)

        parser = Parser(r.content)
        lang_full_name = get_full_lang(lang)
        nodes = parser.query('//a[contains(@href, "/subtitles/%s/%s/")]' % (movie_slug_name, lang_full_name))

        # pprint(nodes)

        # subtitle_match_str = ' '.join(sorted(params['movie_file_tokens']))
        subtitle_match_tokens = set(params['movie_file_tokens'])
        # print 'subtitle_match_str', subtitle_match_str

        subtitles = []
        for node in nodes:
            subtitle_url = node.get('href')
            subtitle_name = node.find('span[2]').text.strip()

            tmp1 = set(tokenizer(subtitle_name))
            # print 'sub match', tmp1
            # d = distance.levenshtein(subtitle_match_str, tmp1)
            d = len(subtitle_match_tokens.intersection(tmp1)) * 100 - len(tmp1)

            subtitles.append({
                'url': urljoin(movie_url, subtitle_url),
                'name': subtitle_name,
                'd': d
            })

        subtitles.sort(key=lambda sub: -sub['d'])

        # pprint(subtitles)

        # if subtitles:
        #     return subtitles[0]

        return subtitles

    def _download_movie_subtitle(self, movie_file, save_dir):
        self.logger.debug('Find subtitle for: %s' % movie_file)
        # print 'movie file', movie_file
        params = {
            'movie_file': movie_file
        }
        tokens = tokenizer(movie_file)
        # print 'tokens', tokens

        params['movie_file_tokens'] = tokens

        movie_title_tokens = []
        for token in tokens:
            if token in self.not_title_tokens:
                break

            if self.year_pattern.match(token):
                params['year'] = int(token)
                break

            movie_title_tokens.append(token)

        if not movie_title_tokens:
            self.logger.debug('Not found movie title tokens to search')
            raise MovieNotFound(file_name=movie_file, message='Not found movie title tokens to search')

        movie_search_query = ' '.join(movie_title_tokens)
        params['movie_title_search_query'] = movie_search_query

        # print movie_search_query

        movie = self._search_movies(params)
        # print movie

        if not movie:
            raise MovieNotFound(file_name=movie_file, message='Not found movie')

        not_found_langs = []
        for lang in self.languages:
            self.logger.debug('Find lang: %s' % lang)
            subtitles = self._get_movie_subs(movie, params, lang)
            if not subtitles:
                self.logger.debug('Not found subtitle')
                not_found_langs.append((lang, 'Not found subtitle'))
                continue

            found_sub = False
            for subtitle in subtitles:
                try:
                    content = self._get_sub_file(subtitle['url'])
                except SubtitleFileBroken:
                    self.logger.warning('Broken sub: %s' % subtitle['url'])
                    continue

                if content:
                    sub_file = join(save_dir, movie_file + '.vi.srt')
                    open(sub_file, 'w').write(content)
                    self.logger.debug('Success')

                    found_sub = True
                    break
                else:
                    self.logger.debug('Could not get subtitle content')
                    continue

            if not found_sub:
                not_found_langs.append((lang, 'Not found valid subtitle'))

        if not_found_langs:
            raise SubtitleNotFound(movie=movie, params=params, detail=not_found_langs)

        return params

    def scan(self, movie_dir):
        reqs = []
        for root_dir, child_folders, file_names in os.walk(movie_dir):
            # print root_dir, child_folders, file_names
            for file_name in file_names:
                for ext in self.movie_extensions:
                    if file_name.endswith('.%s' % ext) and getsize(join(root_dir, file_name)) >= self.min_movie_size:
                        save_dir = root_dir
                        m = self.movie_file_pattern.search(file_name)
                        if not m:
                            continue

                        movie_file = m.group(1)

                        # Detect if the sub existsed
                        missed_langs = []
                        for lang in self.languages:
                            sub_file = join(root_dir, '%s.%s.srt' % (movie_file, lang))
                            if not exists(sub_file):
                                missed_langs.append(lang)

                        if self.force or missed_langs:
                            reqs.append((movie_file, save_dir))

        for movie_file, save_dir in reqs:
            try:
                ret = self._download_movie_subtitle(movie_file, save_dir)
                yield ret
            except (MovieNotFound, SubtitleNotFound) as e:
                yield e
