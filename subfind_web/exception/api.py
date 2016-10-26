API_ERROR_CODE__UNKNOWN = 500
API_ERROR_CODE__MISS_CONFIG = 501


def failed(message, **kwargs):
    ret = {
        'ok': False,
        'message': message
    }
    ret.update(kwargs)

    return ret


class APIError(Exception):
    code = API_ERROR_CODE__UNKNOWN

    def __init__(self, message, *args, **kwargs):
        super(APIError, self).__init__(*args, **kwargs)
        self.message = message

    def __repr__(self, *args, **kwargs):
        return super(APIError, self).__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.message

    def to_json(self):
        return failed(self.message)


class MissConfigError(APIError):
    code = API_ERROR_CODE__MISS_CONFIG

    def __init__(self, *args, **kwargs):
        super(APIError, self).__init__("Missed config file", *args, **kwargs)
