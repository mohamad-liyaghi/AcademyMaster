import pytest
from enrollments.models import Enrollment
from core.tests.utils import create_account


@pytest.fixture
def create_enrollment(create_course):
    user = create_account(is_active=True)
    return Enrollment.objects.create(
        user=user,
        course=create_course
    )
