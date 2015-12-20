class MovieNotFound(Exception):
    def __init__(self, file_name, message=None, *args, **kwargs):
        super(MovieNotFound, self).__init__(*args, **kwargs)
        self.message = message
        self.file_name = file_name


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
