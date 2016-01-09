subtitle_extensions = [
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
]


def get_subtitle_ext(path):
    if not path:
        return None

    for ext in subtitle_extensions:
        if path.endswith('.%s' % ext):
            return ext

    return None
