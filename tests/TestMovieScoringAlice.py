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
                {'title_query': 'kingsman the secret service', 'year': 2014},
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
                {'title_query': 'inside out', 'year': 2015},
                [
                    {'title': 'Inside Out', 'year': 2011},
                    {'title': 'Inside Out', 'year': 2015},
                ],
                [
                    {'title': 'Inside Out', 'year': 2015},
                    {'title': 'Inside Out', 'year': 2011},
                ],
            ),
            # Same score, the one match year win
            (
                {'title_query': '13', 'year': 2010},
                [
                    {'year': 2013, 'title': '13/13/13'},
                    {'year': 2010, 'title': '13'},
                ],
                [
                    {'year': 2010, 'title': '13'},
                    {'year': 2013, 'title': '13/13/13'},
                ],
            ),
            # Same score, the one match title win
            (
                {'title_query': '13', 'year': 2011},
                [
                    {'year': 2013, 'title': '13/13/13'},
                    {'year': 2011, 'title': '13'},
                ],
                [
                    {'year': 2011, 'title': '13'},
                    {'year': 2013, 'title': '13/13/13'},
                ],
            ),
        ]

        for params, movies, expected_movies in testcases:
            params['title_tokens'] = params['title_query'].split(' ')
            # print(params)
            movie_scoring.sort(params, movies)
            # print(movies)

            for i, movie in enumerate(movies):
                self.assertEqual(expected_movies[i]['title'], movie['title'])
                self.assertEqual(expected_movies[i]['year'], movie['year'])

if __name__ == '__main__':
    unittest.main()
