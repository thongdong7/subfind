import re

from subfind.exception import MovieNotFound
from subfind.tokenizer import tokenizer

movie_extensions = ['mp4', 'mkv']
movie_file_pattern = re.compile('^(.+)\.\w+$')
not_title_tokens = set(['x264', '1080p', '1080', '1080i', '720p', 'hdrip', 'hdtv'])
year_pattern = re.compile('^(19\d{2}|200\d|201\d)$')
movie_title_year_pattern = re.compile('^(.*)(\s+\((\d+)\))$')
season_ep_token_pattern = re.compile('^S\d+E\d+$', re.IGNORECASE)


def parse_release_name(release_name):
    """

    :param release_name: Example: Boardwalk.Empire.S01E01.720p.HDTV.x264-IMMERSE
    :type release_name: str
    :return:
    :rtype: dict
    """
    ret = {
        'release_name': release_name
    }

    tokens = tokenizer(release_name)

    ret['release_tokens'] = tokens

    # Get title_query
    movie_title_tokens = []
    for token in tokens:
        if token in not_title_tokens:
            break

        if year_pattern.match(token):
            ret['year'] = int(token)
            break

        movie_title_tokens.append(token)

    if not movie_title_tokens:
        raise MovieNotFound(release_name=release_name, message='Not found movie title tokens to search')

    ret['title_tokens'] = movie_title_tokens

    movie_search_query = ' '.join(movie_title_tokens)
    ret['title_query'] = movie_search_query

    # Find season_ep
    for token in tokens:
        m = season_ep_token_pattern.search(token)
        if m:
            ret['season_eps'] = token
            break

    return ret


def build_title_query_from_title(title):
    return ' '.join(tokenizer(title))
