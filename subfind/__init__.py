import importlib
import logging
import os
import re
from os.path import join, exists, getsize

from subfind_provider.exception import MovieNotFound, SubtitleNotFound


class SubFind(object):
    def __init__(self, languages, provider, force=False, min_movie_size=None):
        self.force = force
        self.languages = languages

        assert isinstance(languages, list)

        self.movie_extensions = ['mp4', 'mkv']
        self.movie_file_pattern = re.compile('^(.+)\.\w+$')

        # Ignore movie file which size < min_movie_size
        self.min_movie_size = min_movie_size

        self.logger = logging.getLogger(self.__class__.__name__)

        module_name = 'subfind_provider_%s' % provider
        module = importlib.import_module(module_name)
        class_name = '%sFactory' % provider.capitalize()
        clazz = getattr(module, class_name)
        data_provider = clazz()
        self.scenario = data_provider.get_scenario()

    def scan(self, movie_dir):
        reqs = []
        for root_dir, child_folders, file_names in os.walk(movie_dir):
            # print root_dir, child_folders, file_names
            for file_name in file_names:
                for ext in self.movie_extensions:
                    if file_name.endswith('.%s' % ext):
                        if self.min_movie_size and getsize(join(root_dir, file_name)) < self.min_movie_size:
                            # Ignore small movie file
                            continue

                        save_dir = root_dir
                        m = self.movie_file_pattern.search(file_name)
                        if not m:
                            continue

                        release_name = m.group(1)

                        # Detect if the sub exists
                        missed_langs = []
                        for lang in self.languages:
                            sub_file = join(root_dir, '%s.%s.srt' % (release_name, lang))
                            if not exists(sub_file):
                                missed_langs.append(lang)

                        if self.force or missed_langs:
                            reqs.append((release_name, save_dir))

        for release_name, save_dir in reqs:
            try:
                for lang, content in self.scenario.execute(release_name, self.languages):
                    sub_file = '%s.%s.srt' % (release_name, lang)
                    sub_file = join(save_dir, sub_file)
                    open(sub_file, 'w').write(content.encode('utf-8'))

                yield {'release_name': release_name}
            except (MovieNotFound, SubtitleNotFound) as e:
                yield e
