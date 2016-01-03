import importlib
import logging
import os
import re
from abc import ABCMeta, abstractmethod
from os.path import join, exists, getsize

from .exception import MovieNotFound, SubtitleNotFound
from .movie_parser import parse_release_name
from .release.alice import ReleaseScoringAlice
from .scenario import ScenarioManager
from .utils import write_file_content


class BaseProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_sub_file(self, sub_page_url):
        """
        Get subtitle content of `sub_page_url`

        :param sub_page_url:
        :type sub_page_url:
        :return:
        :rtype: str
        """
        pass

    @abstractmethod
    def get_releases(self, release_name, langs):
        """
        Find all releases

        :param release_name:
        :type release_name:
        :param langs:
        :type langs:
        :return: A dictionary which key is lang, value is `release_info`
        :rtype:
        """
        return {}


class SubFind(object):
    def __init__(self, languages, provider_names, force=False, min_movie_size=None):
        self.force = force
        self.languages = languages

        assert isinstance(languages, list)

        self.movie_extensions = ['mp4', 'mkv']

        # Credit to https://github.com/callmehiphop/subtitle-extensions/blob/master/subtitle-extensions.json
        self.subtitle_extensions = [
            ".aqt",
            ".gsub",
            ".jss",
            ".sub",
            ".ttxt",
            ".pjs",
            ".psb",
            ".rt",
            ".smi",
            ".slt",
            ".ssf",
            ".srt",
            ".ssa",
            ".ass",
            ".usf",
            ".idx",
            ".vtt"
        ]

        self.movie_file_pattern = re.compile('^(.+)\.\w+$')

        # Ignore movie file which size < min_movie_size
        self.min_movie_size = min_movie_size

        self.logger = logging.getLogger(self.__class__.__name__)

        scenario_map = {}
        for provider_name in provider_names:
            module_name = 'subfind_provider_%s' % provider_name
            module = importlib.import_module(module_name)
            class_name = '%sFactory' % provider_name.capitalize()
            clazz = getattr(module, class_name)
            data_provider = clazz()
            scenario_map[provider_name] = data_provider.get_scenario()

        self.scenario = ScenarioManager(ReleaseScoringAlice(), scenario_map)

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
                        if not self.force:
                            missed_langs = []
                            for lang in self.languages:
                                found = False
                                for subtitle_extension in self.subtitle_extensions:
                                    sub_file = join(root_dir, '%s.%s.%s' % (release_name, lang, subtitle_extension))
                                    if exists(sub_file):
                                        found = True
                                        break

                                if not found:
                                    missed_langs.append(lang)

                        if self.force or missed_langs:
                            reqs.append((release_name, save_dir))

        for release_name, save_dir in reqs:
            try:
                subtitle_paths = []
                for subtitle in self.scenario.execute(release_name, self.languages):
                    sub_file = '%s.%s.%s' % (release_name, subtitle.lang, subtitle.extension)
                    sub_file = join(save_dir, sub_file)
                    subtitle_paths.append(sub_file)
                    write_file_content(sub_file, subtitle.content)

                yield {'release_name': release_name, 'subtitle_paths': subtitle_paths}
            except (MovieNotFound, SubtitleNotFound) as e:
                yield e
