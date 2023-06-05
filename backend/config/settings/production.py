from .core import *


DEBUG = False
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS'))

# TODO add postgresql'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
