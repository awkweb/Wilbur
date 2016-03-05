from .common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'thomasmeagher',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}