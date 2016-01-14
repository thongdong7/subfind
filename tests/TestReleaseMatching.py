from subfind import parse_release_name
from subfind.exception import ReleaseNotMatchError, RELEASE_NOT_MATCH_ERROR__TITLE, RELEASE_NOT_MATCH_ERROR__SEASONEPS
from subfind.release import check_match_release_info

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class ReleaseMatchingTestCase(unittest.TestCase):
    def test_01(self):
        not_match_testcases = [
            ('Game of Thrones S01E01 Winter Is Coming 1080p 5.1', 'Game of Thrones S01E02 Winter Is Coming 1080p 5.1',
             RELEASE_NOT_MATCH_ERROR__SEASONEPS),
            ('Burnt.2015.1080p.BluRay.6CH.1.8GB.MkvCage', 'Max.2015.1080p.BluRay.x264-MkvCage',
             RELEASE_NOT_MATCH_ERROR__TITLE),
        ]

        for release_name1, release_name2, error_code in not_match_testcases:
            release1 = parse_release_name(release_name1)
            release2 = parse_release_name(release_name2)
            try:
                check_match_release_info(release1, release2)
                self.assertTrue(False, msg="Expect ReleaseNotMatchError exception will be raised")
            except ReleaseNotMatchError as e:
                self.assertEqual(error_code, e.code)
            except Exception as e:
                self.assertTrue(False,
                                msg="Only expected ReleaseNotMatchError exception. Receive '%s'" % e.__class__.__name__)


if __name__ == '__main__':
    unittest.main()
