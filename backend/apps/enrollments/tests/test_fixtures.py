import pytest
from enrollments.models import Enrollment, EnrollmentStatus


@pytest.mark.django_db
def test_create_enrollment(create_enrollment):
    assert Enrollment.objects.count() == 1
    assert create_enrollment.status == EnrollmentStatus.PENDING
