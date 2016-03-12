import logging

from abc import ABCMeta, abstractmethod
from subfind.exception import SubtitleFileBroken


class BaseScenario(object):
    __metaclass__ = ABCMeta

    def __init__(self, provider):
        self.provider = provider

    @abstractmethod
    def execute(self, release_name, langs):
        pass

    def get_releases(self, release_name, langs):
        return self.provider.get_releases(release_name, langs)

    def download_subtitle(self, release, target_folder, release_name):
        return self.provider.download_sub(release, target_folder, release_name)



class BaseScenarioFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_scenario(self):
        pass


class Scenario1(BaseScenario):
    """
    release_name + langs

        1. Get releases by release name
        2. group releases by lang
        3. Foreach group, scoring and select the best one, yield

    """

    def __init__(self, release_scoring, provider):
        super(Scenario1, self).__init__(provider)

        self.release_scoring = release_scoring

    def execute(self, release_name, langs, target_folder):
        releases_by_lang = self.provider.get_releases(release_name, langs)

        for lang in releases_by_lang:
            releases = releases_by_lang[lang]
            if not releases:
                continue

            self.release_scoring.sort(release_name, releases)

            release = releases[0]

            subtitle = self.provider.download_sub(release, target_folder, release_name)
            if subtitle:
                yield subtitle


class ScenarioManager(object):
    def __init__(self, release_scoring, scenario_map):
        self.scenario_map = scenario_map
        self.release_scoring = release_scoring

        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self, release_name, langs, target_folder):
        releases_by_lang = {}
        for provider_name in self.scenario_map:
            scenario = self.scenario_map[provider_name]

            try:
                tmp_releases_by_lang = scenario.get_releases(release_name, langs)
                for lang in tmp_releases_by_lang:
                    if lang not in releases_by_lang:
                        releases_by_lang[lang] = []

                    for release in tmp_releases_by_lang[lang]:
                        # Add provider name to this release so we could use get load the subtitle
                        release['provider'] = provider_name

                        releases_by_lang[lang].append(release)
            except Exception as e:
                self.logger.exception(e)

        for lang in releases_by_lang:
            releases = releases_by_lang[lang]
            if not releases:
                continue
            # pprint(releases)

            self.release_scoring.sort(release_name, releases)
            # print('after scoring')
            # pprint(releases)
            # raise SystemExit

            for release in releases:
                provider_name = release['provider']

                try:
                    subtitle = self.scenario_map[provider_name].download_subtitle(release, target_folder, release_name)
                    if subtitle:
                        yield subtitle
                        break
                except SubtitleFileBroken:
                    continue


class Scenario2(BaseScenario):
    """
    release_name + langs

        1. Get movie by release_name
        2. Get subtitles of movie, group by lang
        3. Foreach group, scoring and select the best one, yield

    """

    def __init__(self, release_scoring, provider):
        self.release_scoring = release_scoring
        self.provider = provider

    def execute(self, release_name, langs, target_folder):
        raise NotImplemented
