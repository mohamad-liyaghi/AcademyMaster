from django.core.exceptions import ValidationError
import pytest
from enrollments.models import Enrollment, EnrollmentStatus


@pytest.mark.django_db
class TestEnrollmentModel:
    def test_enrollment_default_status(self, create_enrollment):
        assert create_enrollment.status == EnrollmentStatus.PENDING

    def test_create_pending_enrollment_twice(self, create_enrollment):
        assert create_enrollment.status == EnrollmentStatus.PENDING
        with pytest.raises(ValidationError):
            Enrollment.objects.create(
                user=create_enrollment.user, course=create_enrollment.course
            )

    def test_create_success_enrollment_twice(self, create_enrollment):
        create_enrollment.status = EnrollmentStatus.SUCCESS
        create_enrollment.save()
        assert create_enrollment.status == EnrollmentStatus.SUCCESS
        with pytest.raises(ValidationError):
            Enrollment.objects.create(
                user=create_enrollment.user, course=create_enrollment.course
            )

    def test_enrollment_has_token(self, create_enrollment):
        assert create_enrollment.token

    def test_enrollment_price(self, create_enrollment):
        course = create_enrollment.course
        assert create_enrollment.price == course.price
        course.price += 100
        course.save()
        create_enrollment.refresh_from_db()
        assert create_enrollment.price != course.price
