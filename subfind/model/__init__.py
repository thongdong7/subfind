class Subtitle(object):
    def __init__(self, lang, content, extension='srt'):
        self.lang = lang
        self.content = content
        self.extension = extension