import logging
import re
from os import listdir
from os.path import join, abspath
from shutil import rmtree
from tempfile import mkdtemp

import requests

from subfind.cmd import run_cmd
from subfind.exception import SubtitleFileBroken
from subfind.parser import Parser
from subfind.provider import BaseProvider
from subfind.provider.subscene.language import get_full_lang
from six.moves.urllib.parse import urlencode, urljoin

SUBSCENE_SEARCH_URL = "http://subscene.com/subtitles/title?%s"


class SubsceneProvider(BaseProvider):
    def __init__(self):
        self.session = requests.Session()

        self.movie_title_year_pattern = re.compile('^(.*)(\s+\((\d+)\))$')

        self.logger = logging.getLogger(self.__class__.__name__)

    def search_movie(self, params):
        query = params['movie_title_search_query']
        base_url = (SUBSCENE_SEARCH_URL % urlencode({'q': query}))

        r = self.session.get(base_url)

        if not r.ok:
            return []

        parser = Parser(r.content)
        nodes = parser.query('//div[@class="title"]/a[contains(@href, "/subtitles/")]')

        movies = []
        processed_urls = set()
        for node in nodes:
            url = node.get('href')
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

            movies.append({
                'title': movie_title,
                'year': movie_year,
                'url': movie_url
            })

        return movies

    def get_movie_subs(self, movie, params, lang):
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
        # subtitle_match_tokens = set(params['movie_file_tokens'])
        # print 'subtitle_match_str', subtitle_match_str

        subtitles = []
        for node in nodes:
            subtitle_url = node.get('href')
            subtitle_name = node.find('span[2]').text.strip()

            # tmp1 = set(tokenizer(subtitle_name))
            # d = len(subtitle_match_tokens.intersection(tmp1)) * 100 - len(tmp1)

            subtitles.append({
                'url': urljoin(movie_url, subtitle_url),
                'name': subtitle_name,
                # 'd': d
            })

        return subtitles

    def get_sub_file(self, sub_page_url):
        r = self.session.get(sub_page_url)
        if not r.ok:
            # print r.content
            return None

        m = re.search('href=\"(/subtitle/download[^\'"]+)"', r.content)
        if not m:
            # print 'Could not find download url'
            return None

        sub_download_url = urljoin(sub_page_url, m.group(1))

        tmp_folder = mkdtemp(prefix='subfind-')
        try:
            tmp_file = abspath(join(tmp_folder, 'tmp.zip'))

            # run_cmd('rm %s/* -rf' % tmp_folder)

            response = requests.get(sub_download_url, stream=True)
            if not response.ok:
                # Something went wrong
                # print 'could not download sub file'
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

