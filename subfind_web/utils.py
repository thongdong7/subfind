import yaml
from os.path import join, exists

import os

home_dir = os.path.expanduser('~')
subfind_config_dir = join(home_dir, '.subfind')

if not exists(subfind_config_dir):
    os.makedirs(subfind_config_dir)

config_path = join(subfind_config_dir, 'subfind.yml')

default_config = {
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


def has_config():
    return exists(config_path)


def get_config():
    if not exists(config_path):
        save_config(default_config)

    return yaml.load(open(config_path))


def save_config(config):
    content = yaml.safe_dump(config)

    open(config_path, 'w').write(content)
