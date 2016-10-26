from genericpath import exists

from os.path import abspath

from six import string_types
from subfind_web.exception.api import APIError


def folder_validator(value):
    tmp_value = abspath(value)
    if not exists(tmp_value):
        raise APIError('Invalid folder %s' % value)

    return tmp_value


def load_validator(name):
    # TODO Fix this
    if name == 'folder_validator':
        return folder_validator

    raise Exception('load_validator(name) need to be implemented')


class ValidatorManager(object):
    def __init__(self, value_validator):
        self.value_validator = self._build_validator(value_validator)

    def _build_validator(self, value_validator):
        ret = {}

        for field in value_validator:
            validator = value_validator[field]
            if isinstance(validator, string_types):
                validator = load_validator(validator)

            ret[field] = validator

        return ret

    def validate_field(self, field_name, value):
        if field_name not in self.value_validator:
            return value

        validator_method = self.value_validator[field_name]
        return validator_method(value)
