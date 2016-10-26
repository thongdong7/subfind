import os
from os.path import expanduser, join, exists

import yaml
from subfind.movie_parser import parse_release_name


class Config(object):
    def __init__(self, config_path=None):
        if not config_path:
            home_dir = expanduser('~')
            subfind_config_dir = join(home_dir, '.subfind')

            if not exists(subfind_config_dir):
                os.makedirs(subfind_config_dir)

            config_path = join(subfind_config_dir, 'subfind.yml')

        self.config_path = config_path

        self.default_config = {
            'src': [],
            'providers': ['opensubtitles', 'subscene'],
            'lang': ['en'],
            'force': False,
            'remove': False,
            'verbose': False,
            # Get maximum 5 subtitles for each release
            'max-sub': 5,
            # ignore files less than 500 MB
            'min-movie-size': 500 * 1024 * 1024,
        }

        self._data = self.get_config()

    def has_config(self):
        return exists(self.config_path)

    def get_config(self):
        if not exists(self.config_path):
            self.save_config(self.default_config)

        return yaml.load(open(self.config_path))

    def update(self, data):
        self._data.update(data)

    def save(self):
        content = yaml.safe_dump(self._data)

        open(self.config_path, 'w').write(content)

    def __getitem__(self, name):
        return self._data[name]

    def to_json(self):
        return self._data


class DataProvider(object):
    def __init__(self, sub_finder, config):
        self.config = config
        self.sub_finder = sub_finder
        self.data = []

    def build_data(self):
        movie_requests = self.sub_finder.build_download_requests_for_movie_dirs(self.config['src'], force=True)

        data = []
        for release_name, movie_dir, langs in movie_requests:
            item = {
                'name': release_name,
                'src': movie_dir,
                'languages': list(langs),
                'subtitles': self.sub_finder.stat_subtitle(release_name, movie_dir)
            }

            item.update(parse_release_name(item['name']))

            data.append(item)

        self.data = sorted(data, key=lambda x: x['name'])
