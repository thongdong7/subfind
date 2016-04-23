from subfind_provider_subscene import get_short_lang

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class LangTestCase(unittest.TestCase):
    def test_01(self):
        self.assertEqual('vi', get_short_lang('vietnamese'))
        self.assertEqual('vi', get_short_lang('Vietnamese'))
        self.assertEqual('en', get_short_lang('English'))
        self.assertEqual(None, get_short_lang('InvalidLang'))


if __name__ == '__main__':
    unittest.main()
