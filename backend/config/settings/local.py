from .core import *
from datetime import timedelta
from decouple import config
DEBUG = True
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS'))


INSTALLED_APPS += [
    'debug_toolbar',
]


MIDDLEWARE += {
    'debug_toolbar.middleware.DebugToolbarMiddleware',
}

INTERNAL_IPS = ["*"]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
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
CELERY_BEAT_SCHEDULE = {
    'auto_delete_expired_verification_codes': {
        'task': 'apps.accounts.tasks.delete_expired_codes',
        'schedule': timedelta(minutes=5),
    },
    'auto_delete_deactiavted_users': {
        'task': 'apps.accounts.tasks.delete_deactivated_users',
        'schedule': timedelta(minutes=5),
    },
    'auto_change_course_status_to_in_progress': {
        'task': 'apps.courses.tasks.change_course_status_to_in_progress',
        'schedule': timedelta(minutes=5),
    },
    'auto_change_course_status_to_completed': {
        'task': 'apps.courses.tasks.change_course_status_to_completed',
        'schedule': timedelta(minutes=5),
    },
}


MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'
