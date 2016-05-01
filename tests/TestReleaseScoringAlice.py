from subfind.release.alice import ReleaseScoringAlice

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class ReleaseScoringAliceTestCase(unittest.TestCase):
    def test_01(self):
        """
        Release which match the movie title should be the higher priority

        :return:
        :rtype:
        """
        scoring = ReleaseScoringAlice()
        input_release_name = 'Survivor.2014.1080p.BluRay.H264.AAC-RARBG'

        found_releases = [
            {'name': 'The.Hobbit.The.Battle.of.the.Five.Armies.2014.1080p.BluRay.H264.AAC-RARBG'},
            {'name': 'Survivor.2015.1080p.BluRay.H264.AAC-RARBG'},
        ]
        scoring.sort(input_release_name, found_releases)

        self.assertEqual('Survivor.2015.1080p.BluRay.H264.AAC-RARBG', found_releases[0]['name'])

    def test_02(self):
        """
        Test 100% match

        :return:
        :rtype:
        """
        scoring = ReleaseScoringAlice()
        input_release_name = '400.Days.2015.1080p.BluRay.H264.AAC-RARBG'

        found_releases = [
            {'name': '400.Days.2015.1080p.BluRay.H264.AAC-RARBG'},
            {'name': '400.Days.2015.720p.BluRay.H264.AAC-RARBG'},
            {'name': '400.Days.2015.BRRip.XviD.AC3-RARBG'},
            {'name': '400.Days.2015.1080p.BluRay.H264.AAC-RARBG'},
            {'name': '400.Days.2015.720p.BluRay.x264.[YTS.AG]'},
        ]
        scoring.sort(input_release_name, found_releases)
        # pprint(found_releases)

        self.assertEqual('400.Days.2015.1080p.BluRay.H264.AAC-RARBG', found_releases[0]['name'])

    def test_03(self):
        """
        Test release team match

        :return:
        :rtype:
        """
        scoring = ReleaseScoringAlice()
        input_release_name = 'Lost.in.the.Sun.2015.1080p.BluRay.x264.AAC-ETRG'

        found_releases = [
            {'name': 'Lost.in.the.Sun.2015.WEB-DL.XviD.MP3-RARBG'},
            {'name': 'Lost.in.the.Sun.2015.WEB-DL.x264-RARBG.mp4'},
            {'name': 'Lost.in.the.Sun.2015.HDRip.XviD-ETRG'},
        ]
        scoring.sort(input_release_name, found_releases)
        # pprint(found_releases)

        self.assertEqual('Lost.in.the.Sun.2015.HDRip.XviD-ETRG', found_releases[0]['name'])

if __name__ == '__main__':
    unittest.main()
