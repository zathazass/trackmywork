from .base import *
from .logger_setup import PRODUCTION_LOGGING


SECRET_KEY = config('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES['default'] = convert_to_dict()

LOGGING = PRODUCTION_LOGGING
