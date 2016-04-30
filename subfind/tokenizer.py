import re


def tokenizer(text):
    tokens = re.compile('[\s\.\-_\[\]/:]+').split(text.lower())

    ret = []
    for token in tokens:
        if token:
            ret.append(token)

    return ret
