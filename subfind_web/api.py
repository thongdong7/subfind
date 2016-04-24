import json
from functools import update_wrapper

from flask import Response


def api(func):
    def func_wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        content = json.dumps(data)

        return Response(content, mimetype='application/json')

    return update_wrapper(func_wrapper, func)
    return func_wrapper
