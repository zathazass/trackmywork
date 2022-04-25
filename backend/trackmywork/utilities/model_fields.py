from django.db import models
from trackmywork.utilities.funcs import encrypt_data, decrypt_data


class ConfidentialField(models.BinaryField):
    description = "Encrypted Binary Value"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1024
        kwargs['blank'] = False
        kwargs['null'] = False
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_data(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_data(value)

    def to_python(self, value):
        if value is None:
            return value
        return decrypt_data(value)
