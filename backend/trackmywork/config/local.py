from .base import *


DEBUG = True

ALLOWED_HOSTS = []

# DATABASES['default'] = convert_to_dict(env=config('DJANGO_DB_DEFAULT_URL'))
DATABASES['default'] = convert_to_dict()
