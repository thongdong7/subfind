from subfind_cli.utils import RewriteLine

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class UtilsTestCase(unittest.TestCase):
    def test_01(self):
        rewrite_line = RewriteLine()
        rewrite_line.rewrite('hello')
        rewrite_line.rewrite('hell')
        rewrite_line.rewrite('hello world')
        rewrite_line.newline()
        rewrite_line.rewrite('xin chao')


if __name__ == '__main__':
    unittest.main()
