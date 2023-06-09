from .core import *


DEBUG = True
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('TEST_DATABASE_NAME'),
        'USER': config('TEST_DATABASE_USER'),
        'PASSWORD': config('TEST_DATABASE_PASSWORD'),
        'HOST': config('TEST_DATABASE_HOST'),
        'PORT': config('TEST_DATABASE_PORT')
    }
}
