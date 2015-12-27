from subfind.provider.subscene import SubsceneProvider

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class SubsceneTestCase(unittest.TestCase):
    def setUp(self):
        self.provider = SubsceneProvider()

    def test_search_movie(self):
        movies = self.provider.search_movie({
            'movie_title_search_query': 'the hobbit'
        })

        # pprint(movies)

        self.assertIsNotNone(movies)
        self.assertTrue(isinstance(movies, list))
        self.assertTrue(len(movies) > 0)

    def test_get_movie_subs(self):
        movie = {'title': 'The Hobbit: An Unexpected Journey',
                 'url': 'http://subscene.com/subtitles/the-hobbit-an-unexpected-journey',
                 'year': 2012}
        params = {}
        subtitles = self.provider.get_movie_subs(movie, params, 'en')

        # pprint(subtitles)

        self.assertTrue(subtitles is not None)
        self.assertTrue(isinstance(subtitles, list))
        self.assertTrue(len(subtitles) > 0)

    def test_get_sub_file(self):
        content = self.provider.get_sub_file('http://subscene.com/subtitles/the-divergent-series-insurgent/vietnamese/1151452')

        self.assertIsNotNone(content)

if __name__ == '__main__':
    unittest.main()
