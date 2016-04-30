class MovieNotFound(Exception):
    def __init__(self, release_name, message=None, *args, **kwargs):
        super(MovieNotFound, self).__init__(*args, **kwargs)
        self.message = message
        self.release_name = release_name

    def __str__(self):
        return '%s: %s' % (self.message, self.release_name)

    def __repr__(self):
        return self.__str__()


class SubtitleNotFound(Exception):
    def __init__(self, movie, params, detail=None, *args, **kwargs):
        super(SubtitleNotFound, self).__init__(*args, **kwargs)
        self.movie = movie
        self.params = params
        self.detail = detail


class SubtitleFileBroken(Exception):
    def __init__(self, url, message=None, *args, **kwargs):
        super(SubtitleFileBroken, self).__init__(*args, **kwargs)
        self.message = message
        self.url = url


class ReleaseMissedLangError(Exception):
    def __init__(self, release_name, missed_langs, found_langs, *args, **kwargs):
        super(ReleaseMissedLangError, self).__init__(*args, **kwargs)
        self.found_langs = found_langs
        self.release_name = release_name
        self.missed_langs = missed_langs


RELEASE_NOT_MATCH_ERROR__SEASONEPS = 100
RELEASE_NOT_MATCH_ERROR__TITLE = 101


class ReleaseNotMatchError(Exception):
    def __init__(self, code, *args, **kwargs):
        super(ReleaseNotMatchError, self).__init__(*args, **kwargs)
        self.code = code


class HTTPConnectionError(Exception):
    def __repr__(self, url, return_code, body, *args, **kwargs):
        self.url = url
        self.return_code = return_code
        self.body = body
        return super(HTTPConnectionError, self).__repr__(*args, **kwargs)
