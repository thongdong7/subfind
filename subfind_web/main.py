import json

import os
from flask import Flask, jsonify, Response, request
import logging

from subfind import parse_release_name, SubFind
from subfind.event import EventManager
from subfind_web.crossdomain import crossdomain

app = Flask(__name__)

languages = ['vi']
providers = ['subscene']
# providers = ['opensubtitles', 'subscene']
force = False
remove = False
min_movie_size = 0
max_sub = 5

event_manager = EventManager()

sub_finder = SubFind(event_manager, languages=languages, provider_names=providers, force=force, remove=remove,
                     min_movie_size=min_movie_size, max_sub=max_sub)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/release")
@crossdomain(origin='*')
def release():
    data = [
        {'name': 'Avengers.Age.of.Ultron.2015.1080p.BluRay.x264.YIFY'}
    ]

    for item in data:
        item.update(parse_release_name(item['name']))

    content = json.dumps(data)
    # print(content)

    return Response(content, mimetype='application/json')


@app.route("/release/download")
@crossdomain(origin='*')
def release_download():
    movie_dir = request.args.get('dir')

    sub_finder.scan_movie_dir(movie_dir)

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
