import pytest
from enrollments.models import Enrollment, EnrollmentStatus


@pytest.mark.django_db
def test_create_enrollment(create_enrollment):
    assert Enrollment.objects.count() == 1
    assert create_enrollment.status == EnrollmentStatus.PENDING

@pytest.mark.django_db
def test_create_success_enrollment(create_success_enrollment):
    assert Enrollment.objects.count() == 1
    assert create_success_enrollment.status == EnrollmentStatus.SUCCESS
