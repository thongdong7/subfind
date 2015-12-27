from abc import ABCMeta, abstractmethod


class BaseProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_movie(self, params):
        """
        Find all movies match with `params.movie_title_search_query`.
        This is not 100% percent match. A scoring will find the best match movie

        :param params:
        :type params:
        :return:
        :rtype:
        """
        pass

    @abstractmethod
    def get_movie_subs(self, movie, params, lang):
        """
        Get subtitles for movie

        :param movie:
        :type movie:
        :param params:
        :type params:
        :param lang:
        :type lang:
        :return:
        :rtype:
        """

    @abstractmethod
    def get_sub_file(self, sub_page_url):
        """
        Get subtitle content of `sub_page_url`

        :param sub_page_url:
        :type sub_page_url:
        :return:
        :rtype:
        """
        pass
