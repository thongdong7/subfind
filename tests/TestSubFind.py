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
            ('m1', ['vi'], 'Everest.2015.HC.1080p.HDRiP.x264.ShAaNiG.vi.srt', 114130),
            ('m2', ['en'], 'Survivor.2014.1080p.BluRay.H264.AAC-RARBG.en.srt', 77028),
        ]

        for test_dir, languages, sub_file, expected_size in testcases:
            m1_dir = join(self.data_dir, test_dir)
            sub_file_path = join(m1_dir, sub_file)
            if exists(sub_file_path):
                unlink(sub_file_path)

            sub_finder = SubFind(languages=languages, provider='subscene', force=True)

            for item in sub_finder.scan(m1_dir):
                print(item)

            self.assertTrue(exists(sub_file_path))

            sub_size = len(get_file_content(sub_file_path))
            self.assertEqual(expected_size, sub_size)

            unlink(sub_file_path)


if __name__ == '__main__':
    unittest.main()
