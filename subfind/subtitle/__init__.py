from abc import ABCMeta, abstractmethod


class SubtitleScoring(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, movie, params, subtitles):
        pass
