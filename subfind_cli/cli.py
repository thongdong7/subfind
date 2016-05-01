import logging
import os
import sys
from os.path import exists

import click
import yaml

from subfind.finder import SubFind
from subfind.event import EventManager
from subfind_cli.utils import ReleaseOutput, error_msg


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    pass


default_min_movie_size = 500
mb = 1024 * 1024
default_providers = ['opensubtitles', 'subscene']


@click.command('scan', help='Scan movie directories')
@click.option('--movie-dir', '-d', required=False, multiple=True, help='Movie directories (support multiple)')
@click.option('-l', '--lang', required=False, multiple=True,
              help='Language (support multiple). E.g.: -l en -l vi')
@click.option('--providers', '-p', multiple=True, default=default_providers,
              help='Subtitle provider. E.g: -p opensubtitles -p subscene. Default is opensubtitles and subscene.')
@click.option('-f', '--force', is_flag=True, help='Force to override the existed subtitles')
@click.option('-r', '--remove', is_flag=True, help='Remove olf subtitle if not found.'
                                                   ' Only affect when --force is enabled')
@click.option('-v', '--verbose', is_flag=True, help='Verbose')
@click.option('--min-movie-size', default=default_min_movie_size * mb,
              help='Min movie size. Default: %sMB' % default_min_movie_size)
@click.option('--max-sub', default=1,
              help='Maximum subtitle for each release.')
def cli_scan(movie_dir, lang, providers, force, remove, verbose, min_movie_size, max_sub):
    scan(movie_dir, lang, providers, force, remove, verbose, min_movie_size, max_sub)


def scan(movie_dir, lang, providers, force, remove, verbose, min_movie_size, max_sub):
    # print(movie_dir, lang, providers, force, remove, verbose, min_movie_size, max_sub)
    # sys.exit(1)
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    if isinstance(lang, str):
        languages = lang.split(',')
    else:
        languages = lang

    event_manager = EventManager()
    ReleaseOutput(event_manager, languages)

    sub_finder = SubFind(event_manager, languages=languages, provider_names=providers, force=force, remove=remove,
                         min_movie_size=min_movie_size, max_sub=max_sub)

    sub_finder.scan(movie_dir)


@click.command('scan-config', help='Load parameters from config file to scan')
@click.option('--config', '-c', 'config_file', required=False,
              help='Config file. Default: subfind in current working dir'
                   ' or $HOME/.subfind/subfind.yml')
def cli_scan_config(config_file):
    scan_config(config_file)


def scan_config(config_file):
    if not config_file:
        config_file = 'subfind.yml'
        if not exists(config_file):
            config_file = '%s/.subfind/subfind.yml' % (os.getenv('HOME'))
            if not exists(config_file):
                error_msg('Could not found subfind.yml in current folder and $HOME/.subfind/subfind.yml')
                sys.exit(1)
    elif not exists(config_file):
        error_msg('File %s does not exists' % config_file)
        sys.exit(1)

    # Build params
    try:
        data = yaml.load(open(config_file))
    except Exception as e:
        error_msg('Could not load config file: %s' % str(e))
        sys.exit(2)

    movie_dir = data.get('src')
    lang = data.get('lang')
    providers = data.get('providers', default_providers)
    force = data.get('force', False)
    remove = data.get('remove', False)
    verbose = data.get('verbose', False)
    min_movie_size = data.get('min-movie-size', default_min_movie_size * mb)
    max_sub = data.get('max-sub', 1)

    if isinstance(movie_dir, str):
        movie_dir = [movie_dir]

    # Validate require params
    fields = [
        (movie_dir, 'movie directories'),
        (lang, 'languages'),
        (providers, 'subtitle providers'),
    ]
    for obj, error_text in fields:
        if not obj:
            error_msg('Missed %s' % error_text)
            sys.exit(2)

    scan(movie_dir, lang, providers, force, remove, verbose, min_movie_size, max_sub)


cli.add_command(cli_scan)
cli.add_command(cli_scan_config)

if __name__ == '__main__':
    cli()
