import os
from os.path import expanduser, join, exists, getmtime

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
            self._data = self.default_config
            self.save()

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
        for sub_request in movie_requests:
            item = {
                'name': sub_request.release_name,
                'src': sub_request.save_dir,
                'languages': list(sub_request.languages),
                'subtitles': self.sub_finder.stat_subtitle(sub_request.release_name, sub_request.save_dir),
                'modification_time': getmtime(sub_request.movie_path)
            }

            item.update(parse_release_name(item['name']))

            data.append(item)

        self.data = sorted(data, key=lambda x: -x['modification_time'])
