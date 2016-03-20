import os

from django.core.wsgi import get_wsgi_application

from wilbur.keys import SETTINGS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS)

application = get_wsgi_application()
