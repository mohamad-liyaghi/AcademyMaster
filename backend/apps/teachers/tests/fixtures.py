import pytest
from teachers.models import Teacher
from core.tests.utils import create_account


@pytest.fixture(scope="class")
def teacher_account(django_db_blocker, django_db_setup):
    with django_db_blocker.unblock():
        user = create_account(is_active=True)
        Teacher.objects.create(user=user)
        yield user
