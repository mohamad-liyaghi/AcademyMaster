import pytest
from enrollments.models import Enrollment, EnrollmentStatus
from core.tests.utils import create_account


@pytest.fixture(scope="class")
def create_enrollment(create_course, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = create_account(is_active=True)
        return Enrollment.objects.create(user=user, course=create_course)


@pytest.fixture(scope="class")
def create_success_enrollment(create_course, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = create_account(is_active=True)
        return Enrollment.objects.create(
            user=user, course=create_course, status=EnrollmentStatus.SUCCESS
        )
