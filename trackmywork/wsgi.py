import os
from trackmywork.setenv import PRODUCTION, BASE

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', BASE)

application = get_wsgi_application()
