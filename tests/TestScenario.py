import shutil
from os.path import exists, getsize

from subfind.utils import get_file_content
from subfind_provider_subscene import SubsceneFactory
from tempfile import mkdtemp

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class ScenarioTestCase(unittest.TestCase):
    def test_01(self):
        scenario = SubsceneFactory().get_scenario()
        return
        testcases = [
            # Format: release_name, lang, expected_extension, expected_size
            # (
            #     'Boardwalk.Empire.S01E01.720p.HDTV.x264-IMMERSE', 'en', 'srt', 79325
            # ),
            # (
            #     'Burnt.2015.1080p.BluRay.6CH.1.8GB.MkvCage', 'vi', 'srt', 75313
            # ),
            # (
            #     'Lost.in.the.Sun.2015.1080p.BluRay.x264.AAC-ETRG', 'en', 'srt', 75313
            # ),
            (
                'Hotel.Transylvania.2.2015.1080p.HDRip.1.5GB.MkvCage', 'en', 'srt', 75313
            ),
        ]

        for release_name, lang, expected_extension, expected_size in testcases:
            sub_dir = mkdtemp()
            try:
                result = scenario.execute(release_name, langs=[lang], target_folder=sub_dir)
                for subtitle in result:
                    self.assertEqual(subtitle.lang, lang)

                    # print(get_file_content(subtitle.path))

                    # self.assertTrue(exists(subtitle.path))
                    # self.assertEqual(expected_extension, subtitle.extension)
                    # self.assertEqual(expected_size, getsize(subtitle.path))
            finally:
                shutil.rmtree(sub_dir)




if __name__ == '__main__':
    unittest.main()
