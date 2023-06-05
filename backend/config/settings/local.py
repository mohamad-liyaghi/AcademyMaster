from .core import *


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
