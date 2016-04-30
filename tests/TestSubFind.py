from os import unlink
from os.path import dirname, join, abspath, exists

from subfind import EVENT_RELEASE_COMPLETED
from subfind.finder import SubFind, EVENT_RELEASE_COMPLETED
from subfind.event import EventManager
from subfind.utils import get_file_content

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
called_release_completed = False


class SubFindTestCase(unittest.TestCase):
    def test_01(self):
        global called_release_completed
        self.data_dir = abspath(join(dirname(__file__), 'data'))

        testcases = [
            ('m1', ['vi'], 'Everest.2015.HC.1080p.HDRiP.x264.ShAaNiG.vi.srt'),
            ('m2', ['en'], 'Survivor.2014.1080p.BluRay.H264.AAC-RARBG.en.srt'),
        ]

        for test_dir, languages, sub_file in testcases:
            m1_dir = join(self.data_dir, test_dir)
            sub_file_path = join(m1_dir, sub_file)
            if exists(sub_file_path):
                unlink(sub_file_path)

            event_manager = EventManager()
            called_release_completed = False

            def release_completed(event):
                global called_release_completed
                called_release_completed = True
                self.assertTrue('subtitle_paths' in event)
                self.assertTrue(len(event['subtitle_paths']) > 0)
                for subtitle_path in event['subtitle_paths']:
                    # print(subtitle_path)
                    self.assertTrue(exists(subtitle_path))

                    sub_size = len(get_file_content(subtitle_path))
                    self.assertTrue(sub_size > 0)

                    unlink(subtitle_path)

            event_manager.register(EVENT_RELEASE_COMPLETED, release_completed)

            sub_finder = SubFind(event_manager, languages=languages, provider_names=['opensubtitles', 'subscene'],
                                 force=True)

            sub_finder.scan([m1_dir])

            self.assertTrue(called_release_completed)


if __name__ == '__main__':
    unittest.main()
