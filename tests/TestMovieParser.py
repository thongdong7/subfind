# encoding=utf-8
import logging
import unittest

from subfind.movie_parser import parse_release_name

__author__ = 'hiepsimu'

logging.basicConfig(level=logging.DEBUG)


class MovieParserTestCase(unittest.TestCase):
    def test_01(self):
        testcases = [
            ('Blade Runner (1982) Final Cut 1080p BluRay.x264 SUJAIDR', {'year': 1982}),
        ]

        for release_name, expected in testcases:
            actual = parse_release_name(release_name)
            # pprint(actual)
            for field in expected:
                self.assertEqual(expected[field], actual.get(field),
                                 "Field '{0}' in {1} does not match".format(field, release_name))


if __name__ == '__main__':
    unittest.main()
