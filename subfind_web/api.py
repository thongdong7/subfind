import json
from functools import update_wrapper

from flask import Response
from subfind_web.exception.api import APIError


def failed(message):
    return {
        'ok': False,
        'message': message
    }


def api(func):
    def func_wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
        except APIError as e:
            data = failed(str(e))

        content = json.dumps(data)

        return Response(content, mimetype='application/json')

    return update_wrapper(func_wrapper, func)
