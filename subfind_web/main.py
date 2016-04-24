import logging

import os
from flask import Flask, request
from subfind import parse_release_name, SubFind
from subfind.event import EventManager
from subfind_web.api import api
from subfind_web.crossdomain import crossdomain
from subfind_web.utils import save_config, get_config
from subfind_web.validate import folder_validator, ValidatorManager

app = Flask(__name__)

config = get_config()

event_manager = EventManager()

sub_finder = SubFind(event_manager, languages=config['lang'],
                     provider_names=config['providers'], force=config['force'],
                     remove=config['remove'],
                     min_movie_size=config['min-movie-size'], max_sub=config['max-sub'])

data = []


def build_data():
    global data
    movie_requests = sub_finder.build_download_requests_for_movie_dirs(config['src'])

    data = []
    for release_name, movie_dir, langs in movie_requests:
        item = {
            'name': release_name,
            'src': movie_dir,
            'languages': langs,
            'subtitles': sub_finder.stat_subtitle(release_name, movie_dir)
        }

        item.update(parse_release_name(item['name']))

        data.append(item)

    data = sorted(data, key=lambda x: x['name'])


build_data()


# print(data)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/release")
@crossdomain(origin='*')
@api
def release():
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

    for field_name in ['src', 'lang']:
        push_value = request.args.get('%s-$push' % field_name)
        if push_value:
            push_value = validator_manager.validate_field(field_name, push_value)
            # add_src_abs = abspath(add_src)
            # if not exists(add_src_abs):
            #     raise APIError("Invalid folder %s" % add_src)

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

    sub_finder.scan_movie_dir(save_dir)

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
    # watch(join(root_dir, 'data/postgresql'))
    # watch(join(root_dir, 'generated'))

    ioloop.start()
