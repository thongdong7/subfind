import logging

import sys

import os
import re
from flask import Flask, request, render_template
from os.path import join, abspath, dirname
from subfind.event import EventManager
from subfind.finder import SubFind
from subfind.movie_parser import parse_release_name
from subfind_web.api import api
from subfind_web.crossdomain import crossdomain
from subfind_web.exception.api import MissConfigError
from subfind_web.utils import save_config, get_config, has_config
from subfind_web.validate import folder_validator, ValidatorManager
from tornado.autoreload import watch

if getattr(sys, 'frozen', False):
    current_folder = abspath(dirname(sys.executable))
elif __file__:
    current_folder = abspath(os.path.dirname(__file__))


template_folder = join(current_folder, 'templates')
static_folder = abspath(join(current_folder, 'static'))

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)


@app.route('/node_modules/<path:filename>')
def node_files(filename):
    return app.send_static_file(join('node_modules', filename))


@app.route('/js/<path:filename>')
def dist_files(filename):
    return app.send_static_file(join('client/dist', filename))


config = get_config()

event_manager = EventManager()

sub_finder = SubFind(event_manager, languages=config['lang'],
                     provider_names=config['providers'], force=config['force'],
                     remove=config['remove'],
                     min_movie_size=config['min-movie-size'], max_sub=config['max-sub'])

data = []


def build_data():
    global data
    movie_requests = sub_finder.build_download_requests_for_movie_dirs(config['src'], force=True)

    data = []
    for release_name, movie_dir, langs in movie_requests:
        item = {
            'name': release_name,
            'src': movie_dir,
            'languages': list(langs),
            'subtitles': sub_finder.stat_subtitle(release_name, movie_dir)
        }

        item.update(parse_release_name(item['name']))

        data.append(item)

    data = sorted(data, key=lambda x: x['name'])


build_data()

# print(data)
port_pattern = re.compile(':\d+')
ip_pattern = re.compile('^[\d\.]+$')


@app.route("/")
def homepage():
    host = request.headers['Host']
    domain = port_pattern.sub('', host)

    if ip_pattern.match(domain):
        is_production = True
    else:
        is_production = False

    return render_template("layout.html", domain=domain, is_production=is_production)


@app.route("/release")
@crossdomain(origin='*')
@api
def release():
    if not has_config():
        global config

        config = get_config()

        raise MissConfigError()

    return data


@app.route("/config")
@crossdomain(origin='*')
@api
def get_config():
    return config


value_validator = {
    'src': folder_validator
}

validator_manager = ValidatorManager(value_validator)


@app.route("/config/update")
@crossdomain(origin='*')
@api
def config_update():
    update = {}

    for field_name in ['src', 'lang', 'providers']:
        push_value = request.args.get('%s-$push' % field_name)
        if push_value:
            push_value = validator_manager.validate_field(field_name, push_value)

            tmp = set(config[field_name])
            tmp.add(push_value)
            update[field_name] = sorted(list(tmp))

        remove_value = request.args.get('%s-$remove' % field_name)
        if remove_value:
            remove_value = validator_manager.validate_field(field_name, remove_value)

            tmp = set(config[field_name])
            if remove_value in tmp:
                tmp.remove(remove_value)
                update[field_name] = sorted(list(tmp))

    for bool_field in ['force', 'remove']:
        bool_value = request.args.get(bool_field)
        if bool_value is None:
            continue

        if bool_value == 'true':
            bool_value = True
        else:
            bool_value = False

        update[bool_field] = bool_value

    for int_field in ['min-movie-size', 'max-sub']:
        int_value = request.args.get(int_field)
        if int_value is None:
            continue

        try:
            int_value = int(int_value)
        except ValueError:
            continue

        update[int_field] = int_value

    config.update(update)

    save_config(config)

    if 'src' in update:
        build_data()

    return config


@app.route("/release/scan-all")
@crossdomain(origin='*')
def release_scan_all():
    sub_finder.scan(config['src'])

    build_data()

    return 'Completed'


@app.route("/release/download")
@crossdomain(origin='*')
def release_download():
    save_dir = request.args.get('src')
    release_name = request.args.get('name')

    sub_finder.scan_movie_dir(save_dir, release_name=release_name)

    build_data()

    return 'Completed'


@app.route("/release/remove-subtitle")
@crossdomain(origin='*')
def release_remove_subtitle():
    save_dir = request.args.get('src')
    release_name = request.args.get('name')

    sub_finder.remove_subtitle(save_dir, release_name=release_name)

    build_data()

    return 'Completed'


if __name__ == "__main__":
    from tornado import autoreload
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    DEFAULT_APP_TCP_PORT = 5000

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s', )

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(DEFAULT_APP_TCP_PORT)
    ioloop = IOLoop.instance()
    autoreload.start(ioloop)

    root_dir = os.path.abspath(os.path.dirname(__file__))
    watch(join(root_dir, 'data/postgresql'))
    # watch(join(root_dir, 'generated'))

    ioloop.start()
