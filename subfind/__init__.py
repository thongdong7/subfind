import logging

import importlib
import os
import re
import shutil
from abc import ABCMeta, abstractmethod
from os.path import join, exists, getsize
from subfind.model import Subtitle
from subfind.processor import SingleSubtitleProcessor, MultipleSubtitleProcessor
from subfind.utils.subtitle import subtitle_extensions, remove_subtitle, get_subtitle_info
from .exception import MovieNotFound, SubtitleNotFound, ReleaseMissedLangError
from .movie_parser import parse_release_name
from .release.alice import ReleaseScoringAlice
from .scenario import ScenarioManager
from .utils import write_file_content

EVENT_SCAN_RELEASE = 'SCAN_RELEASE'
EVENT_RELEASE_FOUND_LANG = 'RELEASE_FOUND_LANG'
EVENT_RELEASE_COMPLETED = 'RELEASE_COMPLETED'
EVENT_RELEASE_MOVIE_NOT_FOUND = 'RELEASE_MOVIE_NOT_FOUND'
EVENT_RELEASE_SUBTITLE_NOT_FOUND = 'RELEASE_SUBTITLE_NOT_FOUND'


class BaseProvider(object):
    __metaclass__ = ABCMeta

    # @abstractmethod
    # def download_sub(self, release, target_folder, release_name):
    #     """
    #     Download subtitle of `release` and save to target folder. Name of subtitle will base on the release name,
    #      language and subtitle file format.
    #
    #     :param release:
    #     :type release:
    #     :param target_folder:
    #     :type target_folder:
    #     :param release_name:
    #     :type release_name:
    #     :return:
    #     :rtype: str
    #     """
    #     pass

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

    @abstractmethod
    def get_sub(self, sub_release):
        """
        Get subtitle

        :param sub_release:
        :type sub_release:
        :return:
        :rtype: subfind.model.Subtitle
        """
        pass

    def _save_sub(self, release, sub_file, target_folder, release_name, sub_extension):
        desc_sub_file = join(target_folder, '%s.%s.%s' % (release_name, release['lang'], sub_extension))

        shutil.copyfile(sub_file, desc_sub_file)
        return Subtitle(path=desc_sub_file, lang=release['lang'], extension=sub_extension)


class SubFind(object):
    def __init__(self, event_manager, languages, provider_names, force=False, remove=False, min_movie_size=None, max_sub=1):
        """

        :param event_manager:
        :type event_manager: subfind.event.EventManager
        :param languages:
        :type languages:
        :param provider_names:
        :type provider_names:
        :param force:
        :type force:
        :param remove:
        :type remove:
        :param min_movie_size:
        :type min_movie_size:
        :return:
        :rtype:
        """
        self.max_sub = max_sub
        self.remove = remove
        self.event_manager = event_manager
        self.force = force
        assert isinstance(languages, list) or isinstance(languages, set)

        if isinstance(languages, list):
            self.languages = set(languages)
        else:
            self.languages = languages

        self.movie_extensions = ['mp4', 'mkv']

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

        self.subtitle_processor = MultipleSubtitleProcessor()

    def stat_subtitle(self, release_name, movie_dir):
        """
        Count how many subtitles by languages

        :param release_name:
        :type release_name:
        :param movie_dir:
        :type movie_dir:
        :return:
        :rtype:
        """
        ret = {}
        for root_dir, child_folders, file_names in os.walk(movie_dir):
            for file_name in file_names:
                if not file_name.startswith(release_name):
                    continue

                subtitle_info = get_subtitle_info(file_name)
                if not subtitle_info:
                    continue

                if 'lang' not in subtitle_info:
                    continue

                lang = subtitle_info['lang']
                if lang not in ret:
                    ret[lang] = []

                ret[lang].append(file_name)

        # Sort result
        for lang in ret:
            ret[lang] = sorted(ret[lang])

        return ret

    def build_download_requests(self, movie_dir):
        reqs = []
        for root_dir, child_folders, file_names in os.walk(movie_dir):
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
                                for subtitle_extension in subtitle_extensions:
                                    sub_file = join(root_dir, '%s.%s.%s' % (release_name, lang, subtitle_extension))
                                    if exists(sub_file):
                                        found = True
                                        break

                                if not found:
                                    missed_langs.append(lang)

                        if self.force:
                            reqs.append((release_name, save_dir, self.languages))
                        elif missed_langs:
                            reqs.append((release_name, save_dir, missed_langs))

        return reqs

    def build_download_requests_for_movie_dirs(self, movie_dirs):
        reqs = []
        for movie_dir in movie_dirs:
            reqs += self.build_download_requests(movie_dir)

        return reqs

    def process_download_requests(self, reqs):
        for release_name, save_dir, search_langs in reqs:
            try:
                subtitle_paths = []
                # found_langs = set()
                self.event_manager.notify(EVENT_SCAN_RELEASE, (release_name, search_langs))

                # print(self.scenario, self.max_sub)
                found_subs_by_lang = self.scenario.execute(release_name, search_langs, max_sub=self.max_sub)
                params = {
                    'release_name': release_name,
                    'save_dir': save_dir,
                    'force': self.force,
                    'remove': self.remove,
                }
                for lang in found_subs_by_lang:
                    params['lang'] = lang
                    params['subtitles'] = found_subs_by_lang[lang]
                    self.subtitle_processor.process(**params)

                    if params['subtitles']:
                        self.event_manager.notify(EVENT_RELEASE_FOUND_LANG, (release_name, lang))

                # for subtitle in self.scenario.execute(release_name, search_langs, save_dir):
                #     found_langs.add(subtitle.lang)
                #
                #     subtitle_paths.append(subtitle.path)
                #
                #     self.event_manager.notify(EVENT_RELEASE_FOUND_LANG, (release_name, subtitle))

                # if self.force and self.remove:
                #     # Remove subtitle of missed lang
                #     not_found_langs = set(search_langs).difference(found_langs)
                #     for lang in not_found_langs:
                #         remove_subtitle(save_dir, release_name, lang)

                self.event_manager.notify(EVENT_RELEASE_COMPLETED, {
                    'release_name': release_name,
                    'subtitle_paths': subtitle_paths,
                })
            except MovieNotFound as e:
                self.event_manager.notify(EVENT_RELEASE_MOVIE_NOT_FOUND, e)
            except SubtitleNotFound as e:
                self.event_manager.notify(EVENT_RELEASE_SUBTITLE_NOT_FOUND, e)

    def scan_movie_dir(self, movie_dir):
        reqs = self.build_download_requests(movie_dir)

        self.process_download_requests(reqs)

    def scan(self, movie_dirs):
        reqs = self.build_download_requests_for_movie_dirs(movie_dirs)

        self.process_download_requests(reqs)
