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

if __name__ == '__main__':
    unittest.main()
