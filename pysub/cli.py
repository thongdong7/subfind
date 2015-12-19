import logging

from pysub.exception import MovieNotFound, SubtitleNotFound
from pysub.subscene import SubFinder
from clint.textui import puts, indent, colored


def error_msg(text):
    puts(colored.red(text))


def info_msg(text):
    puts(colored.green(text))


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Subtitle Finder')
    parser.add_argument('-d', dest='movie_dir', help='Movie directory')
    parser.add_argument('-l', dest='lang', help='Languages. Multiple languages separated by comma (,). E.g.: en,vi')

    args = parser.parse_args()

    languages = args.lang.split(',')

    # print args
    # raise SystemExit

    sub_finder = SubFinder(languages=languages)

    # sub_finder._download_movie_subtitle('Inside.Out.2015.1080p.BluRay.x264.YIFY', '/data2/movies/Inside Out (2015) [1080p]/')
    # return

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
    logging.basicConfig(level=logging.WARNING)
    main()
