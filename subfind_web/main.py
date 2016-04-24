import logging
from os.path import abspath, exists

import os
from flask import Flask, request
from subfind import parse_release_name, SubFind
from subfind.event import EventManager
from subfind_web.api import api
from subfind_web.crossdomain import crossdomain
from subfind_web.exception.api import APIError

app = Flask(__name__)

languages = ['vi']
providers = ['subscene']
# providers = ['opensubtitles', 'subscene']
force = False
remove = False
# ignore files less than 500 MB
min_movie_size = 500 * 1024 * 1024
max_sub = 5
src_dirs = ["/data2/movies"]

config = {
    'src': src_dirs,
    'lang': languages,
    'force': force,
    'remove': remove,
    'max-sub': max_sub
}

event_manager = EventManager()

sub_finder = SubFind(event_manager, languages=languages, provider_names=providers, force=force, remove=remove,
                     min_movie_size=min_movie_size, max_sub=max_sub)

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
    # print(data)
    # print(movie_requests)
    #
    # data = [
    #     {'name': 'Avengers.Age.of.Ultron.2015.1080p.BluRay.x264.YIFY'}
    # ]

    # for item in data:
    #     item.update(parse_release_name(item['name']))

    return data


@app.route("/config")
@crossdomain(origin='*')
@api
def get_config():
    return config


@app.route("/config/update")
@crossdomain(origin='*')
@api
def config_update():
    update = {}

    add_src = request.args.get('src-$push')
    if add_src:
        add_src_abs = abspath(add_src)
        if not exists(add_src_abs):
            raise APIError("Invalid folder %s" % add_src)

        src = set(config['src'])
        src.add(add_src_abs)
        update['src'] = sorted(list(src))

    remove_src = request.args.get('src-$remove')
    if remove_src:
        remove_src_abs = abspath(remove_src)
        if not exists(remove_src_abs):
            raise APIError("Invalid folder %s" % remove_src)

        src = set(config['src'])
        if remove_src_abs in src:
            src.remove(remove_src_abs)
            update['src'] = sorted(list(src))

    config.update(update)

    if 'src' in update:
        build_data()

    return config


@app.route("/release/scan-all")
@crossdomain(origin='*')
def release_scan_all():
    sub_finder.scan(src_dirs)

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
