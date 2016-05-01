from os import unlink

import yaml
from os.path import dirname, join, abspath
from subfind.utils import write_file_content
from subfind_cli.cli import scan_config

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class CliScanConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.data_dir = abspath(join(dirname(__file__), 'data'))

    def test_01(self):
        cli_dir = join(self.data_dir, 'cli1')
        config_file = join(cli_dir, 'subfind.yml')
        movies_dir_name = ['m1', ',2']
        movies_dir = []
        for movie_dir_name in movies_dir_name:
            movies_dir.append(join(self.data_dir, movie_dir_name))

        write_file_content(config_file, yaml.safe_dump({
            'src': movies_dir,
            'force': True,
            'lang': ['vi', 'en'],
            'min-movie-size': 0,
            'providers': ['opensubtitles', 'subscene']
        }))

        scan_config(config_file)

        unlink(config_file)


if __name__ == '__main__':
    unittest.main()
