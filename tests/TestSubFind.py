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

        testcases = [
            ('m1', ['vi'], 'Everest.2015.HC.1080p.HDRiP.x264.ShAaNiG.vi.srt'),
            ('m2', ['en'], 'Survivor.2014.1080p.BluRay.H264.AAC-RARBG.en.srt'),
        ]

        for test_dir, languages, sub_file in testcases:
            m1_dir = join(self.data_dir, test_dir)
            sub_file_path = join(m1_dir, sub_file)
            if exists(sub_file_path):
                unlink(sub_file_path)

            sub_finder = SubFind(languages=languages, provider='subscene', force=True)

            for item in sub_finder.scan(m1_dir):
                print(item)

            self.assertTrue(exists(sub_file_path))

            sub_size = len(get_file_content(sub_file_path))
            self.assertTrue(sub_size > 0)

            unlink(sub_file_path)


if __name__ == '__main__':
    unittest.main()
