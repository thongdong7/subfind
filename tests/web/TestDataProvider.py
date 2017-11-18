# encoding=utf-8
from os import unlink
from pprint import pprint

import yaml
from os.path import dirname, join, abspath
from subfind.utils import write_file_content
from subfind_cli.cli import scan_config
from subfind_web.model.config import DataProvider
from tb_ioc import IOC

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


@unittest.skip
class CliScanConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.data_dir = abspath(join(dirname(__file__), '../data'))

    def test_01(self):
        ioc = IOC()
        ioc.load_resource('@subfind_web')
        ioc.put('Config', {
            'lang': ['en'],
            'providers': ['opensubtitles', 'subscene'],
            # 'src': [join(self.data_dir, 'm3')],
            'src': ['/data2/movies'],
            'force': True,
            'remove': False,
            'min-movie-size': 0,
            'max-sub': 1,
        })

        data_provider = ioc.get('DataProvider')
        data_provider.build_data()

        pprint(data_provider.data)
        found = False
        for item in data_provider.data:
            if item['name'] == 'Mr.Robot.S02E01.720p.HDTV.x264-KILLERS':
                found = True
                print(item)
        # self.assertEqual(1, len(data_provider.data))
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
