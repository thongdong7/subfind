import shutil
from abc import ABCMeta, abstractmethod
from os.path import join


class SubtitleProcessor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, release_name, save_dir, lang, force, remove, subtitles):
        """
        Process the subtitles

        :param subtitles:
        :type subtitles:
        :param remove:
        :type remove:
        :param force:
        :type force:
        :param lang:
        :type lang:
        :param save_dir:
        :type save_dir:
        :param release_name:
        :type release_name:
        :return:
        :rtype:
        """


class SingleSubtitleProcessor(SubtitleProcessor):
    """
    Save the first subtitle
    """

    def __init__(self):
        pass

    def process(self, release_name, save_dir, lang, force, remove, subtitles):
        if not subtitles:
            return

        subtitle = subtitles[0]
        desc_sub_file = join(save_dir, '%s.%s.%s' % (release_name, lang, subtitle.extension))

        if subtitle.path:
            shutil.copyfile(subtitle.path, desc_sub_file)
            # return Subtitle(path=desc_sub_file, lang=release['lang'], extension=sub_extension)
        else:
            print(desc_sub_file, subtitle.content.__class__)
            # write_file_content(desc_sub_file, subtitle.content)
            open(desc_sub_file, 'wb').write(subtitle.content)


class MultipleSubtitleProcessor(SubtitleProcessor):
    """
    Save multiple subtitles
    """

    def __init__(self):
        pass

    def process(self, release_name, save_dir, lang, force, remove, subtitles):
        if not subtitles:
            return

        for i, subtitle in enumerate(subtitles):
            desc_sub_file = join(save_dir, '%s.%s.%s.%s' % (release_name, i, lang, subtitle.extension))

            if subtitle.path:
                shutil.copyfile(subtitle.path, desc_sub_file)
            else:
                open(desc_sub_file, 'wb').write(subtitle.content)
