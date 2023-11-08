import pytest
from datetime import date
from courses.models import Course
from core.models import WeekDays


@pytest.fixture(scope="class")
def create_course(superuser, teacher_account, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        yield Course.objects.create(
            title="test title",
            description="test description",
            location="test location",
            instructor=teacher_account.teacher,
            assigned_by=superuser,
            start_date=date(2023, 10, 30),
            end_date=date(2023, 11, 30),
            days=[WeekDays.SATURDAY.value],
        )
