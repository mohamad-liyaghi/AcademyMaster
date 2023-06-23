import pytest
from teachers.models import Teacher
from core.tests.utils import create_account


@pytest.fixture
def teacher_account():
    user = create_account(is_active=True)
    Teacher.objects.create(
        user=user
    )
    return user
