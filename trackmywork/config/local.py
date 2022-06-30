from .base import *
from .logger_setup import LOCAL_LOGGING

DEBUG = True

ALLOWED_HOSTS = []

# DATABASES['default'] = convert_to_dict(env=config('DJANGO_DB_DEFAULT_URL'))
DATABASES['default'] = convert_to_dict()

LOGGING = LOCAL_LOGGING
