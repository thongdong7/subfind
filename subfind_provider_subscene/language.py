lang_map = {
    'en': 'english',
    'vi': 'vietnamese',
}

short_lang_map = dict(zip(lang_map.values(), lang_map.keys()))


def get_full_lang(name):
    return lang_map[name]


def get_short_lang(name):
    return short_lang_map.get(name.strip().lower())
