import encodings
import os
import pkgutil
import sys


def all_encodings():
    modnames = set(
            [modname for importer, modname, ispkg in pkgutil.walk_packages(
                    path=[os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)


encodings = all_encodings()


def get_file_content(path):
    if sys.version_info >= (3, 0):
        for enc in encodings:
            try:
                with open(path, encoding=enc) as f:
                    return f.read()
            except Exception:
                pass
    else:
        return open(path).read()
