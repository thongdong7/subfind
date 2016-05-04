API_ERROR_CODE__UNKNOWN = 500
API_ERROR_CODE__MISS_CONFIG = 501


class APIError(Exception):
    code = API_ERROR_CODE__UNKNOWN

    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def __repr__(self, *args, **kwargs):
        return super().__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.message


class MissConfigError(APIError):
    code = API_ERROR_CODE__MISS_CONFIG

    def __init__(self, *args, **kwargs):
        super().__init__("Missed config file", *args, **kwargs)


