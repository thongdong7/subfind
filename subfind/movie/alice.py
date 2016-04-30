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

a_win = -1
b_win = 1
no_one_win = 0


def movie_match_year(arbiter_year, a, b):
    if a['year'] != b['year']:
        # Which one is the same with arbiter_year win
        if a['year'] == arbiter_year:
            return a_win
        elif b['year'] == arbiter_year:
            return b_win

    return no_one_win


def movie_match_display_title(arbiter_title_query, a, b):
    if a['display_title_query'] == arbiter_title_query:
        return a_win

    if b['display_title_query'] == arbiter_title_query:
        return b_win

    return no_one_win


def movie_match_title(arbiter_title_query, a, b):
    if a['title_query'] == arbiter_title_query:
        return a_win

    if b['title_query'] == arbiter_title_query:
        return b_win

    return no_one_win


class MovieScoringAlice(MovieScoring):
    def sort(self, params, movies):
        query_tokens = set(params['title_tokens'])
        arbiter_year = params['year']
        arbiter_title_query = params['title_query']

        for movie in movies:
            self.build_score(movie, query_tokens, 'title', 'title_query', 'title_d')
            if 'display_title' in movie:
                self.build_score(movie, query_tokens, 'display_title', 'display_title_query', 'display_title_d')
            # movie['title_query'] = build_title_query_from_title(movie['title'])
            # # movie['d'] = distance.levenshtein(query, movie['title'].lower()),
            # # Switch to jaccard index because it's more accuracy.
            # # Failed case of distance.levenshtein() is 'men in black ii' vs 'men in black iii'
            # movie_title_tokens = set(tokenizer(movie['title_query']))
            #
            # movie['d'] = 1 - float(len(query_tokens.intersection(movie_title_tokens))) / len(query_tokens.union(movie_title_tokens))

        def movie_cmp(a, b):
            # important
            if 'display_title_query' in a and 'display_title_query' in b:
                display_title_score = movie_match_display_title(arbiter_title_query, a, b)
            else:
                display_title_score = no_one_win
                
            title_score = movie_match_title(arbiter_title_query, a, b)
            year_score = movie_match_year(arbiter_year, a, b)

            # print(display_title_score, title_score, year_score)

            # title_score better than year_score
            final_score = display_title_score + 2 * title_score + year_score
            if final_score < 0:
                return a_win
            elif final_score > 0:
                return b_win

            # Case: Both movies have wrong year
            if a['year'] != arbiter_year and b['year'] != arbiter_year:
                # The one match title_query win
                if a['title_query'] == arbiter_title_query:
                    return a_win
                elif b['title_query'] == arbiter_title_query:
                    return b_win

                if a['year'] > b['year']:
                    # larger year is better
                    return a_win
                elif a['year'] < b['year']:
                    return b_win
            else:
                if a['year'] != b['year']:
                    # Which one is the same with arbiter_year win
                    if a['year'] == arbiter_year:
                        return a_win
                    elif b['year'] == arbiter_year:
                        return b_win

            if a['display_title_d'] < b['display_title_d']:
                # smaller distances is better
                return a_win
            elif a['display_title_d'] > b['display_title_d']:
                return b_win

            if a['title_d'] < b['title_d']:
                # smaller distances is better
                return a_win
            elif a['title_d'] > b['title_d']:
                return b_win

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

    def is_match(self, params, movie):
        if 'year' in params and 'year' in movie:
            if abs(movie['year'] - params['year']) > 1:
                # the year of movie too different
                return False

        return True
