from subfind.utils.subtitle import get_subtitle_info

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class SubtitleUtilsTestCase(unittest.TestCase):
    def test_01(self):
        testcases = [
            ('', None),
            ('srt', None),
            ('abc.srt', {'ext': 'srt'}),
            ('abc.vi.srt', {'ext': 'srt', 'lang': 'vi'}),
        ]

        for file_name, expected_result in testcases:
            ret = get_subtitle_info(file_name)
            self.assertEqual(expected_result, ret)


if __name__ == '__main__':
    unittest.main()
