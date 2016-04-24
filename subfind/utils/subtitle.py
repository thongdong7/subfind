# Credit to https://github.com/callmehiphop/subtitle-extensions/blob/master/subtitle-extensions.json
import os

from os.path import join, exists

subtitle_extensions = set([
    "aqt",
    "gsub",
    "jss",
    "sub",
    "ttxt",
    "pjs",
    "psb",
    "rt",
    "smi",
    "slt",
    "ssf",
    "srt",
    "ssa",
    "ass",
    "usf",
    "idx",
    "vtt"
])

languages_code = set([
    'en', 'vi'
])


def get_subtitle_ext(path):
    if not path:
        return None

    for ext in subtitle_extensions:
        if path.endswith('.%s' % ext):
            return ext

    return None


def remove_subtitle(path, release_name, lang):
    for ext in subtitle_extensions:
        sub_file = join(path, '%s.%s.%s' % (release_name, lang, ext))
        if exists(sub_file):
            os.unlink(sub_file)


def get_subtitle_info(file_name):
    if not file_name:
        return None

    tokens = file_name.split('.')
    if len(tokens) < 2 or tokens[-1] not in subtitle_extensions:
        # Not subtitle file
        return None

    ret = {
        'ext': tokens[-1],
    }

    if tokens[-2] in languages_code:
        ret['lang'] = tokens[-2]

    return ret
