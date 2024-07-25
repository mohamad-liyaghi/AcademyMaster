import pytest
from django.conf import settings
from config.celery import celery
from apps.core.tests.fixtures import *
from apps.accounts.tests.fixtures import *
from apps.managers.tests.fixtures import *
from apps.teachers.tests.fixtures import *
from apps.courses.tests.fixtures import *
from apps.enrollments.tests.fixtures import *
from apps.activities.tests.fixtures import *


@pytest.fixture(autouse=True, scope="session")
def disable_celery_tasks():
    """
    Disable celery tasks for all tests.
    """
    celery.conf.CELERY_ALWAYS_EAGER = True
    yield
    celery.conf.CELERY_ALWAYS_EAGER = False
