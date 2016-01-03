# -*- coding: utf-8 -*-
from os import unlink

from subfind.utils import get_file_content, write_file_content

__author__ = 'hiepsimu'
import logging
import unittest

from os.path import dirname, join, abspath, exists, getsize

logging.basicConfig(level=logging.DEBUG)


class GetUnicodeFileContentTestCase(unittest.TestCase):
    def setUp(self):
        self.data_dir = abspath(join(dirname(__file__), 'data', 't1'))

    def test_01(self):
        content = get_file_content(join(self.data_dir, 'a.txt'))
        # print(content)

        content = content.strip()
        # The following command does not work with python 3.2
        expected_result = u'Đi nào, đi nào'
        self.assertEqual(expected_result, content)

    def test_02(self):
        path = join(self.data_dir, 'b.txt')
        content = u'Đi nào, đi nào'
        write_file_content(path, content)

        self.assertTrue(exists(path))
        self.assertEqual(18, getsize(path))

        unlink(path)


if __name__ == '__main__':
    unittest.main()
