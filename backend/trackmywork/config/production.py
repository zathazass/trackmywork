from .base import *

SECRET_KEY = config('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES['default'] = convert_to_dict()
