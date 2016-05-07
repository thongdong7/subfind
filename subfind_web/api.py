import json

from flask import Response
from functools import update_wrapper
from subfind_web.exception.api import APIError


def failed(**kwargs):
    ret = {
        'ok': False,
    }

    ret.update(kwargs)

    return ret


def api(func):
    def func_wrapper(*args, **kwargs):
        http_code = 200

        try:
            data = func(*args, **kwargs)
        except APIError as e:
            http_code = 500
            data = failed(message=str(e), code=e.code)

        content = json.dumps(data)

        return Response(content, status=http_code, mimetype='application/json')

    return update_wrapper(func_wrapper, func)
