import pytest
from teachers.models import Teacher


@pytest.fixture
def teacher_account(active_account):
    Teacher.objects.create(
        user=active_account
    )
    return active_account
