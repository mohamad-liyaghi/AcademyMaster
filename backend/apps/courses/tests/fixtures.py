import pytest
from datetime import date
from courses.models import Course
from core.models import WeekDays


@pytest.fixture
def create_course(superuser, teacher_account):
    return Course.objects.create(
        title='test title',
        description='test description',
        location='test location',
        instructor=teacher_account.teacher,
        assigned_by=superuser,
        start_date=date(2023, 10, 30),
        end_date=date(2023, 11, 30),
        days=[WeekDays.SATURDAY.value]
    )
