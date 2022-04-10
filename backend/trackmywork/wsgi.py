import os
from trackmywork.setenv import PRODUCTION

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', PRODUCTION)

application = get_wsgi_application()
