from .core import *
from decouple import config
import logging.config
from django.utils.log import DEFAULT_LOGGING
from datetime import timedelta
from celery.schedules import crontab

DEBUG = False
ALLOWED_HOSTS = list(config("ALLOWED_HOSTS"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
    }
}


LOGGING_CONFIG = None


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/critical.log",
                "formatter": "default",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "": {
                "level": "WARNING",
                "handlers": ["file"],
            },
            "app": {
                "level": "CRITICAL",
                "handlers": ["file"],
                "propagate": False,
            },
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
}

# Celery beat configs
CELERY_BEAT_SCHEDULE = {
    "auto_delete_expired_verification_codes": {
        "task": "apps.accounts.tasks.delete_expired_codes",
        "schedule": crontab(hour=4, minute=0),
    },
    "auto_delete_deactivated_users": {
        "task": "apps.accounts.tasks.delete_deactivated_users",
        "schedule": crontab(hour=5, minute=0),
    },
    "auto_change_course_status_to_in_progress": {
        "task": "apps.courses.tasks.change_course_status_to_in_progress",
        "schedule": crontab(hour=6, minute=0),
    },
    "auto_change_course_status_to_completed": {
        "task": "apps.courses.tasks.change_course_status_to_completed",
        "schedule": crontab(hour=7, minute=0),
    },
    "auto_delete_pending_enrollment": {
        "task": "apps.enrollments.tasks.auto_delete_pending_enrollment",
        "schedule": crontab(hour=7, minute=30),
    },
}

MEDIA_ROOT = "media/"
MEDIA_URL = "/media/"
