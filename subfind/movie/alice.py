from subfind.movie import MovieScoring
from subfind.movie_parser import build_title_query_from_title
from subfind.tokenizer import tokenizer


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


class MovieScoringAlice(MovieScoring):
    a_win = -1
    b_win = 1

    def sort(self, params, movies):
        query_tokens = set(params['title_tokens'])
        arbiter_year = params['year']
        arbiter_title_query = params['title_query']

        for movie in movies:
            self.build_score(movie, query_tokens, 'title', 'title_query', 'title_d')
            self.build_score(movie, query_tokens, 'display_title', 'display_title_query', 'display_title_d')
            # movie['title_query'] = build_title_query_from_title(movie['title'])
            # # movie['d'] = distance.levenshtein(query, movie['title'].lower()),
            # # Switch to jaccard index because it's more accuracy.
            # # Failed case of distance.levenshtein() is 'men in black ii' vs 'men in black iii'
            # movie_title_tokens = set(tokenizer(movie['title_query']))
            #
            # movie['d'] = 1 - float(len(query_tokens.intersection(movie_title_tokens))) / len(query_tokens.union(movie_title_tokens))

        def movie_cmp(a, b):
            # Case: Both movies have wrong year
            if a['year'] != arbiter_year and b['year'] != arbiter_year:
                # The one match title_query win
                if a['title_query'] == arbiter_title_query:
                    return self.a_win
                elif b['title_query'] == arbiter_title_query:
                    return self.b_win

                if a['year'] > b['year']:
                    # larger year is better
                    return self.a_win
                elif a['year'] < b['year']:
                    return self.b_win
            else:
                if a['year'] != b['year']:
                    # Which one is the same with arbiter_year win
                    if a['year'] == arbiter_year:
                        return self.a_win
                    elif b['year'] == arbiter_year:
                        return self.b_win

            if a['display_title_d'] < b['display_title_d']:
                # smaller distances is better
                return self.a_win
            elif a['display_title_d'] > b['display_title_d']:
                return self.b_win

            if a['title_d'] < b['title_d']:
                # smaller distances is better
                return self.a_win
            elif a['title_d'] > b['title_d']:
                return self.b_win

            # Same score now

            return 0

        movies.sort(key=cmp_to_key(movie_cmp))

    @staticmethod
    def build_score(movie, query_tokens, field_name, query_field_name, score_field_name):
        movie[query_field_name] = build_title_query_from_title(movie[field_name])
        # movie['d'] = distance.levenshtein(query, movie['title'].lower()),
        # Switch to jaccard index because it's more accuracy.
        # Failed case of distance.levenshtein() is 'men in black ii' vs 'men in black iii'
        movie_title_tokens = set(tokenizer(movie[query_field_name]))

        movie[score_field_name] = 1 - float(len(query_tokens.intersection(movie_title_tokens))) / len(
            query_tokens.union(movie_title_tokens))
