from os import unlink
from os.path import dirname, join, abspath, exists
from subfind.event import EventManager
from subfind.finder import SubFind, EVENT_RELEASE_FOUND_LANG

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
found_lang_flag = False


class SubFindTestCase(unittest.TestCase):
    def test_01(self):
        self.data_dir = abspath(join(dirname(__file__), 'data'))

        testcases = [
            ('m1', ['en'], 'Everest.2015.HC.1080p.HDRiP.x264.ShAaNiG.vi.srt'),
            # ('m2', ['en'], 'Survivor.2014.1080p.BluRay.H264.AAC-RARBG.en.srt'),
        ]
        global found_lang_flag

        for test_dir, languages, sub_file in testcases:
            m1_dir = join(self.data_dir, test_dir)
            sub_file_path = join(m1_dir, sub_file)
            if exists(sub_file_path):
                unlink(sub_file_path)

            found_lang_flag = False

            def release_found_lang(event):
                global found_lang_flag
                found_lang_flag = True

                release_name, found_lang = event

                self.assertTrue(sub_file.startswith(release_name))
                self.assertTrue(found_lang in languages)

            event_manager = EventManager()
            event_manager.register(EVENT_RELEASE_FOUND_LANG, release_found_lang)

            sub_finder = SubFind(event_manager, languages=languages, provider_names=['opensubtitles', 'subscene'],
                                 force=True)

            sub_finder.scan([m1_dir])

            self.assertTrue(found_lang_flag)


if __name__ == '__main__':
    unittest.main()
