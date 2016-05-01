import sys

from click import echo, style
from subfind.finder import EVENT_SCAN_RELEASE, EVENT_RELEASE_FOUND_LANG, EVENT_RELEASE_COMPLETED, \
    EVENT_RELEASE_MOVIE_NOT_FOUND, EVENT_RELEASE_SUBTITLE_NOT_FOUND


class RewriteLine(object):
    def __init__(self):
        self.last_line = None
        self.file = sys.stdout

    def rewrite(self, line):
        if self.last_line and line.startswith(self.last_line):
            self.file.write(line[len(self.last_line):])
        else:
            self.file.write('\r{0}'.format(line))

        self.last_line = line
        self.file.flush()

    def write(self, line):
        self.file.write(line)
        self.last_line = line
        self.file.flush()

    def newline(self):
        self.last_line = None
        self.file.write('\n')
        self.file.flush()


class ReleaseOutput(object):
    def __init__(self, event_manager, languages):
        self.languages = languages
        self.event_manager = event_manager
        self.output = RewriteLine()

        self.line_size = 80
        self.release_name = None
        self.found_langs = None
        self.search_langs = None
        self.completed = False

        event_manager.register(EVENT_SCAN_RELEASE, self.show_scan_release)
        event_manager.register(EVENT_RELEASE_FOUND_LANG, self.show_release_found)
        event_manager.register(EVENT_RELEASE_COMPLETED, self.show_release_completed)
        event_manager.register(EVENT_RELEASE_MOVIE_NOT_FOUND, self.show_release_movie_not_found)
        event_manager.register(EVENT_RELEASE_SUBTITLE_NOT_FOUND, self.show_release_subtitle_not_found)

    def show_scan_release(self, event):
        self.release_name, self.search_langs = event
        self.found_langs = []
        self.completed = False

        line = self._format()
        self.output.write(line)

    def _format(self):
        langs_color = []
        lang_size = len(self.languages) - 1
        for lang in self.languages:
            if lang not in self.search_langs:
                # The sub for this lang existed
                langs_color.append(str(style(lang, fg='green')))
                lang_size += len(lang)
            elif lang in self.found_langs:
                langs_color.append(str(style(lang, fg='green')))
                lang_size += len(lang)
            elif self.completed:
                langs_color.append(str(style(lang, fg='red')))
                lang_size += len(lang)
            else:
                langs_color.append(str(style(lang, fg='white')) + '?')
                lang_size += len(lang) + 1

        langs_color_str = '|'.join(langs_color)

        size = self.line_size - len(self.release_name) - lang_size
        if size < 0:
            size = 0

        return '{0}{1}{2}'.format(self.release_name, '.' * size, langs_color_str)

    def show_release_found(self, event):
        release_name, lang = event
        self.found_langs.append(lang)

        self._refresh()

    def _refresh(self):
        self.output.rewrite(self._format())

    def show_release_completed(self, event):
        """

        :param event:
        :type event: dict
        :return:
        :rtype:
        """
        self.completed = True

        self._refresh()
        self.output.newline()

    def show_release_movie_not_found(self, event):
        """

        :param event:
        :type event: subfind.exception.MovieNotFound
        :return:
        :rtype:
        """
        self.output.newline()

    def show_release_subtitle_not_found(self, event):
        """

        :param event:
        :type event: subfind.exception.SubtitleNotFound
        :return:
        :rtype:
        """
        self.output.newline()


def error_msg(text):
    echo(style(text, fg='red'))


def info_msg(text):
    echo(style(text, fg='green'))
