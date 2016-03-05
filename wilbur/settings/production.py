from .common import *

ALLOWED_HOSTS = [
    'www.gowilbur.com',
    'gowilbur.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wilbur',
        'USER': 'wilbur',
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
    }
}