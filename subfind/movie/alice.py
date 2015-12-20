import distance

from subfind.movie import MovieScoring


class MovieScoringAlice(MovieScoring):
    def sort(self, params, movies):
        query = params['movie_title_search_query']

        for movie in movies:
            movie['d'] = distance.levenshtein(query, movie['title'].lower()),

        def movie_cmp(a, b):
            if a['d'] < b['d']:
                # smaller distances is better
                return -1
            elif a['d'] > b['d']:
                return 1

            if a['year'] > b['year']:
                # larger year is better
                return -1
            elif a['year'] < b['year']:
                return 1

            return 0

        movies.sort(cmp=movie_cmp)