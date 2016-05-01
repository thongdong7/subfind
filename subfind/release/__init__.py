from abc import ABCMeta, abstractmethod
from subfind.exception import ReleaseNotMatchError, RELEASE_NOT_MATCH_ERROR__SEASONEPS, RELEASE_NOT_MATCH_ERROR__TITLE
from subfind.movie_parser import parse_release_name


class ReleaseScoring(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, release_name, releases):
        pass


def check_match_release_info(release1, release2):
    # season_eps must match
    if release1.get('season_eps') != release2.get('season_eps'):
        raise ReleaseNotMatchError(code=RELEASE_NOT_MATCH_ERROR__SEASONEPS)

    # movie title must be the same
    if release1.get('title_tokens') != release2.get('title_tokens'):
        raise ReleaseNotMatchError(code=RELEASE_NOT_MATCH_ERROR__TITLE)

    return True


class ReleaseMatchingChecker(object):
    def __init__(self, name):
        self.name = name

        self.info = parse_release_name(name)

    def check(self, release_name):
        item_info = parse_release_name(release_name)

        check_match_release_info(self.info, item_info)

        return item_info

