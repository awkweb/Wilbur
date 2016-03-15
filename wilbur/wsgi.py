import os
from wilbur.keys import SETTINGS

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS)

application = get_wsgi_application()
