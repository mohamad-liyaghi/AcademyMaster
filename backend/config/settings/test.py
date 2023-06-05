from .core import *


DEBUG = True
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS'))

# TODO add postgresql'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}