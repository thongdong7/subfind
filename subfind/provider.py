import shutil
from abc import ABCMeta, abstractmethod
from os.path import join
from subfind.model import Subtitle


class BaseProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_releases(self, release_name, langs):
        """
        Find all releases

        :param release_name:
        :type release_name:
        :param langs:
        :type langs:
        :return: A dictionary which key is lang, value is `release_info`
        :rtype:
        """
        return {}

    @abstractmethod
    def get_sub(self, sub_release):
        """
        Get subtitle

        :param sub_release:
        :type sub_release:
        :return:
        :rtype: subfind.model.Subtitle
        """
        pass

    def _save_sub(self, release, sub_file, target_folder, release_name, sub_extension):
        desc_sub_file = join(target_folder, '%s.%s.%s' % (release_name, release['lang'], sub_extension))

        shutil.copyfile(sub_file, desc_sub_file)
        return Subtitle(path=desc_sub_file, lang=release['lang'], extension=sub_extension)
