from subfind.movie_parser import parse_release_name
from subfind.release import ReleaseScoring


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


class ReleaseScoringAlice(ReleaseScoring):
    def sort(self, release_name, releases):
        raw_release_info = parse_release_name(release_name)

        release_tokens = set(raw_release_info['release_tokens'])
        for release in releases:
            release_info = parse_release_name(release['name'])
            release.update(release_info)

            # Jaccard Index - https://en.wikipedia.org/wiki/Jaccard_index
            release['d'] = float(len(release_tokens.intersection(release['release_tokens']))) / len(release_tokens.union(release['release_tokens']))

        def movie_cmp(a, b):
            if a['title_query'] != b['title_query']:
                # The on has same title query (with raw_release_info) is better
                if a['title_query'] == raw_release_info['title_query']:
                    return -1
                elif b['title_query'] == raw_release_info['title_query']:
                    return 1

            if a['d'] > b['d']:
                # larger distances is better
                return -1
            elif a['d'] < b['d']:
                return 1

            if 'year' in a and 'year' in b:
                if a['year'] > b['year']:
                    # larger year is better
                    return -1
                elif a['year'] < b['year']:
                    return 1

            return 0

        releases.sort(key=cmp_to_key(movie_cmp))
