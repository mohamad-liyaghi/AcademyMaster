import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

celery = Celery('config', broker=config("CELERY_BROKER_URL"))
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.config_defaults = {'broker_connection_retry_on_startup': True}

celery.autodiscover_tasks(
    [
        'apps.core.tasks',
        'apps.accounts.task'
     ],
)
