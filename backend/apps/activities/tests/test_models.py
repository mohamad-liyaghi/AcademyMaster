import pytest
from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError
from enrollments.models import EnrollmentStatus
from courses.models import CourseStatus
from activities.models import Activity


@pytest.mark.django_db
class TestActivityModel:
    def test_create_activity(self, create_success_enrollment):
        Activity.objects.all().delete()
        activity = Activity.objects.create(
            user=create_success_enrollment.user, enrollment=create_success_enrollment
        )
        assert activity.course == create_success_enrollment.course
        assert Activity.objects.count() == 1

    def test_create_twice(self, create_success_enrollment):
        assert create_success_enrollment.activities.count() == 1
        with pytest.raises(IntegrityError):
            Activity.objects.create(
                user=create_success_enrollment.user,
                enrollment=create_success_enrollment,
            )

    def test_create_with_others_enrollment(self, create_success_enrollment, superuser):
        Activity.objects.all().delete()
        activity = Activity.objects.create(
            user=superuser, enrollment=create_success_enrollment
        )
        assert activity.user == create_success_enrollment.user
        assert activity.user != superuser

    def test_create_with_failed_enrollment(self, create_enrollment):
        """Raise PermissionDenied if enrollment status is FAILED."""
        create_enrollment.status = EnrollmentStatus.FAILED
        create_enrollment.save()

        assert create_enrollment.status == EnrollmentStatus.FAILED

        with pytest.raises(PermissionDenied):
            Activity.objects.create(
                user=create_enrollment.user, enrollment=create_enrollment
            )

    def test_create_with_pedning_enrollment(self, create_enrollment):
        """Raise PermissionDenied if enrollment status is PENDING."""
        create_enrollment.status = EnrollmentStatus.PENDING
        create_enrollment.save()

        assert create_enrollment.status == EnrollmentStatus.PENDING

        with pytest.raises(PermissionDenied):
            Activity.objects.create(
                user=create_enrollment.user, enrollment=create_enrollment
            )

    def test_create_with_final_mark(self, create_success_enrollment):
        """
        By default final_mark is None
        and teacher cannot change until the course end date.
        """
        Activity.objects.all().delete()
        activity = Activity.objects.create(
            user=create_success_enrollment.user,
            enrollment=create_success_enrollment,
            final_mark=10,
        )
        assert activity.final_mark is None

    def test_add_final_mark_to_unfinished_course(self, get_activity):
        """
        Only activities with course status of COMPLETED can have final_mark.
        """
        assert get_activity.course.status != CourseStatus.COMPLETED
        with pytest.raises(PermissionDenied):
            get_activity.final_mark = 10
            get_activity.save()

    def test_add_final_mark_to_completed_course(self, get_activity):
        get_activity.course.status = CourseStatus.COMPLETED
        get_activity.course.save()
        assert get_activity.course.status == CourseStatus.COMPLETED
        get_activity.final_mark = 10
        get_activity.save()
        assert get_activity.final_mark == 10
