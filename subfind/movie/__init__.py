from abc import ABCMeta, abstractmethod


class MovieScoring(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, params, movies):
        pass


