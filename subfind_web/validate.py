from genericpath import exists

from os.path import abspath
from subfind_web.exception.api import APIError


def folder_validator(value):
    tmp_value = abspath(value)
    if not exists(tmp_value):
        raise APIError('Invalid folder %s' % value)

    return tmp_value


class ValidatorManager(object):
    def __init__(self, value_validator):
        self.value_validator = value_validator

    def validate_field(self, field_name, value):
        if field_name not in self.value_validator:
            return value

        validator_method = self.value_validator[field_name]
        return validator_method(value)
