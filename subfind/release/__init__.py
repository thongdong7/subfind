from abc import ABCMeta, abstractmethod


class ReleaseScoring(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, release_name, releases):
        pass


