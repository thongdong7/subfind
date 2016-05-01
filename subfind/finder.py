import logging
from genericpath import getsize

import importlib
import os
import re
from os.path import join
from subfind.exception import MovieNotFound, SubtitleNotFound
from subfind.processor import MultipleSubtitleProcessor
from subfind.release.alice import ReleaseScoringAlice
from subfind.scenario import ScenarioManager
from subfind.utils.subtitle import get_subtitle_info


EVENT_SCAN_RELEASE = 'SCAN_RELEASE'
EVENT_RELEASE_FOUND_LANG = 'RELEASE_FOUND_LANG'
EVENT_RELEASE_COMPLETED = 'RELEASE_COMPLETED'
EVENT_RELEASE_MOVIE_NOT_FOUND = 'RELEASE_MOVIE_NOT_FOUND'
EVENT_RELEASE_SUBTITLE_NOT_FOUND = 'RELEASE_SUBTITLE_NOT_FOUND'


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
            try:
                module = importlib.import_module(module_name)
            except ImportError:
                self.logger.warn('Invalid module %s' % module_name)
                continue

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

    def build_download_requests(self, movie_dir, release_name=None, force=False):
        reqs = []
        for root_dir, child_folders, file_names in os.walk(movie_dir):
            for file_name in file_names:
                if release_name and not file_name.startswith(release_name):
                    # Not match with the release we need
                    continue

                for ext in self.movie_extensions:
                    if file_name.endswith('.%s' % ext):
                        if self.min_movie_size and getsize(join(root_dir, file_name)) < self.min_movie_size:
                            # Ignore small movie file
                            continue

                        save_dir = root_dir
                        m = self.movie_file_pattern.search(file_name)
                        if not m:
                            continue

                        movie_release_name = m.group(1)

                        # Detect if the sub exists
                        if not force:
                            missed_langs = self._find_missed_langs(movie_release_name, file_names)

                            if missed_langs:
                                reqs.append((movie_release_name, save_dir, missed_langs))
                        else:
                            reqs.append((movie_release_name, save_dir, self.languages))

        return reqs

    def build_download_requests_for_movie_dirs(self, movie_dirs, force=False):
        reqs = []
        for movie_dir in movie_dirs:
            reqs += self.build_download_requests(movie_dir, force=force)

        return reqs

    def process_download_requests(self, reqs):
        for release_name, save_dir, search_langs in reqs:
            try:
                subtitle_paths = []
                self.event_manager.notify(EVENT_SCAN_RELEASE, (release_name, search_langs))

                # print(self.scenario, self.max_sub)
                found_subs_by_lang = self.scenario.execute(release_name, search_langs, max_sub=self.max_sub)
                params = {
                    'release_name': release_name,
                    'save_dir': save_dir,
                    'force': self.force,
                    'remove': self.remove,
                }

                if self.remove:
                    self.remove_subtitle(save_dir, release_name=release_name, langs=found_subs_by_lang.keys())

                for lang in found_subs_by_lang:
                    params['lang'] = lang
                    params['subtitles'] = found_subs_by_lang[lang]
                    self.subtitle_processor.process(**params)

                    if params['subtitles']:
                        self.event_manager.notify(EVENT_RELEASE_FOUND_LANG, (release_name, lang))

                self.event_manager.notify(EVENT_RELEASE_COMPLETED, {
                    'release_name': release_name,
                    'subtitle_paths': subtitle_paths,
                })
            except MovieNotFound as e:
                self.event_manager.notify(EVENT_RELEASE_MOVIE_NOT_FOUND, e)
            except SubtitleNotFound as e:
                self.event_manager.notify(EVENT_RELEASE_SUBTITLE_NOT_FOUND, e)

    def remove_subtitle(self, movie_dir, release_name=None, langs=None):
        for root_dir, child_folders, file_names in os.walk(movie_dir):
            for file_name in file_names:
                sub_info = get_subtitle_info(file_name)
                if not sub_info:
                    continue

                if langs and sub_info.get('lang') not in langs:
                    # This subtitle not belong to remove langs
                    continue

                remove = False
                if release_name:
                    if file_name.startswith(release_name):
                        remove = True
                else:
                    remove = True

                if remove:
                    os.unlink(join(root_dir, file_name))

    def scan_movie_dir(self, movie_dir, release_name=None):
        reqs = self.build_download_requests(movie_dir, release_name=release_name)

        self.process_download_requests(reqs)

    def scan(self, movie_dirs):
        reqs = self.build_download_requests_for_movie_dirs(movie_dirs, force=self.force)

        self.process_download_requests(reqs)

    def _find_missed_langs(self, movie_release_name, file_names):
        found_langs = set()
        for file_name in file_names:
            if not file_name.startswith(movie_release_name):
                continue

            subtitle_info = get_subtitle_info(file_name)
            if not subtitle_info:
                continue

            if 'lang' in subtitle_info:
                found_langs.add(subtitle_info['lang'])

        return self.languages - found_langs



