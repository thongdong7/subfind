# encoding=utf-8
import gevent
from gevent import monkey
from os.path import dirname, abspath, join

from subfind_web.exception.api import APIError
from subfind_web.service.ConfigService import ConfigService

monkey.patch_all()

import json
from functools import wraps
from math import sqrt
from threading import Thread
from time import sleep, time
from flask import Flask, Response, request
from gevent.pywsgi import WSGIServer

from subfind.event import EventManager
from subfind.finder import EVENT_SCAN_RELEASE
from subfind_web.bootstrap import container
from subfind_web.crossdomain import crossdomain
from subfind_web.service.ReleaseService import ReleaseService
from gevent.queue import Queue, Empty


# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):
    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data: "data",
            self.event: "event",
            self.id: "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = []
        for k in self.desc_map:
            if k:
                lines.append("%s: %s" % (self.desc_map[k], k))
        # lines = ["%s: %s" % (v, k)
        #          for k, v in self.desc_map.iteritems() if k]

        return "%s\n\n" % "\n".join(lines)


current_dir = abspath(dirname(__file__))

app = Flask(__name__, static_folder=join(current_dir, 'ui/build'), static_url_path='')
# app = Flask(__name__)

subscriptions = []


@app.route("/")
def index():
    return open(join(current_dir, 'ui/build/index.html')).read()


# Client code consumes like this.
# @app.route("/")
# def index():
#     debug_template = """
#      <html>
#        <head>
#        </head>
#        <body>
#          <h1>Server sent events</h1>
#          <div id="event"></div>
#          <script type="text/javascript">
#
#          var eventOutputContainer = document.getElementById("event");
#          var evtSrc = new EventSource("/subscribe");
#
#          evtSrc.onmessage = function(e) {
#              console.log(e.data);
#              eventOutputContainer.innerHTML = e.data;
#          };
#
#          </script>
#        </body>
#      </html>
#     """
#     return (debug_template)


@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)


def _publish_msg(msg):
    for sub in subscriptions[:]:
        sub.put(msg)


@app.route("/publish")
def publish():
    # Dummy data - pick up from request for real data
    def notify():
        msg = str(time())

        _publish_msg(msg)

    gevent.spawn(notify)

    return "OK"


@app.route("/subscribe")
@crossdomain(origin='*', methods=['GET', 'OPTIONS'])
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        # except GeneratorExit:  # Or maybe use flask signals
        except:
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")


release_service = container.get('ReleaseService')  # type: ReleaseService
config_service = container.get('ConfigService')  # type: ConfigService


def api_response(func):
    @wraps(func)
    def wrapper():
        status_code = 200
        try:
            res = func()
        except APIError as e:
            res = e.to_json()
            status_code = 404

        return Response(json.dumps(res, indent=2), mimetype='application/json', status=status_code)

    return wrapper


@app.route('/api/Release/list')
@api_response
def release_list():
    return release_service.list()


@app.route('/api/Release/download')
@api_response
def release_download():
    ret = release_service.download(src=request.args.get('src'), name=request.args.get('name'))

    _on_scan_release_complete()

    return ret


jobs = Queue()


def _client_action(name, payload):
    return json.dumps(dict(
        type=name,
        payload=payload
    ))


def _push_client_action(name, payload={}):
    return _publish_msg(_client_action(name, payload))


def _on_scan_release(event):
    print('Downloading release {index}/{total} {name}...'.format(
        name=event['release_name'],
        index=event['index'] + 1,
        total=event['total']
    ))
    _push_client_action(name='SCAN_RELEASE', payload=dict(
        releaseName=event['release_name'],
        total=event['total'],
        index=event['index'],
    ))


def _on_scan_release_complete():
    _push_client_action(name='SCAN_RELEASE_COMPLETE')


def _handle_jobs():
    event_manager = container.get('EventManager')  # type: EventManager
    event_manager.register(EVENT_SCAN_RELEASE, _on_scan_release)

    while True:
        try:
            job = jobs.get(timeout=1)

            print('got job', job)

            if job['action'] == 'scan_all':
                release_service.scan_all()

                _on_scan_release_complete()
        except Empty:
            gevent.sleep(1)


@app.route('/api/Release/scan_all')
@api_response
def scan_all():
    jobs.put(dict(
        action="scan_all"
    ))

    return dict(message="posted job")
    # return release_service.scan_all()


@app.route('/api/Config/update')
@api_response
def config_update():
    params = {}
    for field in request.args:
        params[field] = request.args[field]
    return config_service.update(**params)


@app.route('/api/Config/load')
@api_response
def config_load():
    return config_service.index()


def start_web(debug=False, port=32500):
    app.debug = debug

    print('start job handler')
    # t = Thread(target=_handle_jobs)
    # t.start()
    gevent.spawn(_handle_jobs)

    print('start server')
    server = WSGIServer(("", port), app)
    server.serve_forever()


if __name__ == '__main__':
    start_web(debug=True, port=32500)
