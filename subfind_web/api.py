import json

from flask import Response


def api(func):
    def func_wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        content = json.dumps(data)

        return Response(content, mimetype='application/json')

    return func_wrapper
