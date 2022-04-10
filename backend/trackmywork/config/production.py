from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES['default'] = convert_to_dict()
