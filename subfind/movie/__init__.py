from abc import ABCMeta, abstractmethod


class MovieScoring(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def sort(self, params, movies):
        pass

    @abstractmethod
    def is_match(self, params, movie):
        pass

    def get_match(self, params, movies):
        """
        Get matched movies
        
        :param params:
        :type params:
        :param movies:
        :type movies:
        :return:
        :rtype:
        """
        ret = []
        for movie in movies:
            if self.is_match(params, movie):
                ret.append(movie)

        return ret
