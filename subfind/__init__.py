import importlib
import logging
import os
import re
from os.path import join, exists, getsize

from subfind.exception import MovieNotFound, SubtitleNotFound, SubtitleFileBroken
from subfind.movie.alice import MovieScoringAlice
from subfind.subtitle.alice import SubtitleScoringAlice
from subfind.tokenizer import tokenizer

SUBSCENE_SEARCH_URL = "http://subscene.com/subtitles/title?%s"


class SubFinder(object):
    def __init__(self, languages, force=False):
        self.force = force
        self.languages = languages

        assert isinstance(languages, list)

        self.movie_extensions = ['mp4', 'mkv']
        self.movie_file_pattern = re.compile('^(.+)\.\w+$')
        self.not_title_tokens = {'x264', '1080p', '1080', 'hdrip'}
        self.year_pattern = re.compile('^(19\d{2}|201\d)$')
        self.movie_title_year_pattern = re.compile('^(.*)(\s+\((\d+)\))$')

        # Ignore movie file which size < 500MB
        self.min_movie_size = 500 * 1000 * 1000

        self.logger = logging.getLogger(self.__class__.__name__)
        self.movie_scoring = MovieScoringAlice()
        self.subtitle_scoring = SubtitleScoringAlice()

        provider_name = 'subscene'
        module_name = 'subfind_provider_%s' % provider_name
        module = importlib.import_module(module_name)
        class_name = '%sProvider' % provider_name.capitalize()
        clazz = getattr(module, class_name)
        self.data_provider = clazz()

    def _search_movies(self, params):
        movies = self.data_provider.search_movie(params)

        self.movie_scoring.sort(params, movies)

        if movies:
            return movies[0]

        return None

    def _get_sub_file(self, sub_page_url):
        return self.data_provider.get_sub_file(sub_page_url)

    def _get_movie_subs(self, movie, params, lang):
        subtitles = self.data_provider.get_movie_subs(movie, params, lang)

        self.subtitle_scoring.sort(movie, params, subtitles)

        # subtitles.sort(key=lambda sub: -sub['d'])

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
                    sub_file = '%s.%s.srt' % (movie_file, lang)
                    sub_file = join(save_dir, sub_file)
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

                        # Detect if the sub exists
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
