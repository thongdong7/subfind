import logging

from clint.textui import puts, indent, colored

from subfind.exception import MovieNotFound, SubtitleNotFound
from subfind import SubFinder


def error_msg(text):
    puts(colored.red(text))


def info_msg(text):
    puts(colored.green(text))


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Subtitle Finder')
    parser.add_argument('-d', dest='movie_dir', required=True, help='Movie directory')
    parser.add_argument('-l', dest='lang', required=True,
                        help='Languages. Multiple languages separated by comma (,). E.g.: en,vi')
    parser.add_argument('-f', dest='force', action='store_true', help='Force to override the existed subtitles')
    parser.add_argument('-v', dest='verbose', action='store_true', help='Verbose')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    languages = args.lang.split(',')

    sub_finder = SubFinder(languages=languages, force=args.force)

    for item in sub_finder.scan(args.movie_dir):
        if isinstance(item, MovieNotFound):
            error_msg('%s: %s' % (item.file_name, item.message))
        elif isinstance(item, SubtitleNotFound):
            error_msg('%s: Not found sub for following items' % (item.params['movie_file']))
            with indent(4):
                for lang, msg in item.detail:
                    error_msg('%s: %s' % (lang, msg))
        else:

            info_msg('%s: %s' % (item['movie_file'], 'Success'))


if __name__ == '__main__':
    main()
