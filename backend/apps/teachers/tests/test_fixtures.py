import pytest


@pytest.mark.django_db
def test_teacher_is_teacher(teacher_account):
    assert teacher_account.is_teacher()
