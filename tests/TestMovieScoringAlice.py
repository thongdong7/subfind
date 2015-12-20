from subfind.movie.alice import MovieScoringAlice

__author__ = 'hiepsimu'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class MovieScoringAliceTestCase(unittest.TestCase):
    def test_01(self):
        movie_scoring = MovieScoringAlice()
        testcases = [
            # Wrong year, but the title is good
            (
                {'movie_title_search_query': 'kingsman the secret service', 'year': 2014},
                [
                    {'title': 'Kingsman: The Secret Service', 'year': 2015},
                    {'title': "Secrets Of Her Majesty's Secret Service", 'year': 2014},
                ],
                [
                    {'title': 'Kingsman: The Secret Service', 'year': 2015},
                    {'title': "Secrets Of Her Majesty's Secret Service", 'year': 2014},
                ]
            ),
            # The correct year and title should has higher score
            (
                {'movie_title_search_query': 'inside out', 'year': 2015},
                [
                    {'title': 'Inside Out', 'year': 2011},
                    {'title': 'Inside Out', 'year': 2015},
                ],
                [
                    {'title': 'Inside Out', 'year': 2015},
                    {'title': 'Inside Out', 'year': 2011},
                ],
            ),
        ]

        for params, movies, expected_movies in testcases:
            movie_scoring.sort(params, movies)

            for i, movie in enumerate(movies):
                self.assertEqual(expected_movies[i]['title'], movie['title'])
                self.assertEqual(expected_movies[i]['year'], movie['year'])

if __name__ == '__main__':
    unittest.main()
