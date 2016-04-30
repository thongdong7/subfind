class Subtitle(object):
    def __init__(self, extension='srt', path=None, content=None):
        assert path or content

        self.content = content
        self.path = path

        self.extension = extension
