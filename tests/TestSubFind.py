from os import unlink

from os.path import dirname, join, abspath, exists

from subfind import SubFind
from subfind_provider.utils import get_file_content

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class SubFindTestCase(unittest.TestCase):
    def test_01(self):
        self.data_dir = abspath(join(dirname(__file__), 'data'))
        m1_dir = join(self.data_dir, 'm1')
        sub_file = join(m1_dir, 'Everest.2015.HC.1080p.HDRiP.x264.ShAaNiG.vi.srt')
        if exists(sub_file):
            unlink(sub_file)

        sub_finder = SubFind(languages=['vi'], provider='subscene', force=True)

        for item in sub_finder.scan(m1_dir):
            print(item)

        self.assertTrue(exists(sub_file))

        sub_size = len(get_file_content(sub_file))
        self.assertEqual(106842, sub_size)

        unlink(sub_file)


if __name__ == '__main__':
    unittest.main()
