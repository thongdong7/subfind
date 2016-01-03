import re


def tokenizer(text):
    return re.compile('[\s\.\-_\[\]/]+').split(text.lower())