from .core import *
from datetime import timedelta

DEBUG = True
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS'))

THIRD_PARTY_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += {
    'debug_toolbar.middleware.DebugToolbarMiddleware',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT')
    }
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
}

# Celery beat configs
CELERY_BEAT_SCHEDULE = {}
