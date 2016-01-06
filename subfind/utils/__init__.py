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

# Try to parse with utf-8 first
encodings.remove('utf_8')
encodings = ['utf_8'] + list(encodings)


def get_file_content(path):
    if sys.version_info >= (3, 0):
        for enc in encodings:
            try:
                with open(path, encoding=enc) as f:
                    return f.read()
            except Exception:
                pass
    else:
        content = open(path).read()
        try:
            return content.decode('utf-8')
        except:
            return content


def write_file_content(path, content):
    if sys.version_info >= (3, 0):
        try:
            open(path, 'wb').write(content)
        except:
            open(path, 'wb').write(content.encode('utf-8'))
    else:
        try:
            open(path, 'wb').write(content.encode('utf-8'))
        except:
            open(path, 'wb').write(content)

