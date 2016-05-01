from subfind.movie_parser import parse_release_name

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class ParseReleaseNameTestCase(unittest.TestCase):
    def test_01(self):
        testcases = [
            ('Bad.Boys.II.2003.1080.BluRay.X264.YIFY', {'year': 2003, 'title_query': 'bad boys ii'})
        ]

        for release_name, expect_result in testcases:
            ret = parse_release_name(release_name)
            # print(ret)
            for field_name in expect_result:
                self.assertTrue(field_name in ret)
                self.assertEqual(expect_result[field_name], ret[field_name])


if __name__ == '__main__':
    unittest.main()
