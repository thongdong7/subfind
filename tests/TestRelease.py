from pprint import pprint

from subfind_provider_opensubtitles import OpensubtitlesProvider

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class ReleaseTestCase(unittest.TestCase):
    def setUp(self):
        self.provider = OpensubtitlesProvider()

    def test_search_release(self):
        # print(Language.fromopensubtitles('vie'))
        # return
        testcases = [
            ('Survivor.2014.1080p.BluRay.H264.AAC-RARBG', ['en']),
            # ('Boardwalk.Empire.S01E01.720p.HDTV.x264-IMMERSE', ['en', 'vi'])
        ]

        for release_name, langs in testcases:
            releases = self.provider.get_releases(release_name, langs)

            pprint(releases)

            self.assertTrue(releases is not None)
            self.assertTrue(isinstance(releases, dict))
            for lang in releases:
                self.assertTrue(lang in langs)
                self.assertTrue(len(releases[lang]) > 0)


if __name__ == '__main__':
    unittest.main()
