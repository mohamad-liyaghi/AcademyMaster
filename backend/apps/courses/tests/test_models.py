import pytest
from datetime import date
from django.core.exceptions import ValidationError, PermissionDenied
from courses.models import Course, CourseStatus
from core.models import WeekDays


@pytest.mark.django_db
class TestCourseModel:
    @pytest.fixture(autouse=True)
    def setup(self, teacher_account):
        self.data = {
            'title': 'test course',
            'description': 'test description',
            'location': 'test location',
            'instructor': teacher_account.teacher,
            'start_date': date(2023, 9, 30),
            'end_date': date(2023, 10, 30),
            'days': [WeekDays.SATURDAY, WeekDays.SUNDAY],
        }

    def test_create_course(self, accessed_manager_account):
        course = Course.objects.create(
            **self.data, assigned_by=accessed_manager_account
        )
        assert course.assigned_by == accessed_manager_account

    def test_create_course_by_teacher(self, teacher_account):
        '''Only manager/admins with add_course perm can add courses'''
        with pytest.raises(PermissionDenied):
            Course.objects.create(
                **self.data, assigned_by=teacher_account
            )

    def test_create_course_by_manager(self, manager_account):
        '''Only manager/admins with add_course perm can add courses'''
        with pytest.raises(PermissionDenied):
            Course.objects.create(
                **self.data, assigned_by=manager_account
            )

    def test_course_has_token(self, accessed_manager_account):
        course = Course.objects.create(
            **self.data, assigned_by=accessed_manager_account
        )
        assert course.token

    def test_get_days_display(self, accessed_manager_account):
        self.data['days'] = [WeekDays.SATURDAY, WeekDays.SUNDAY]
        course = Course.objects.create(
            **self.data, assigned_by=accessed_manager_account
        )
        assert course.get_days_display == [
            WeekDays.SATURDAY.label, WeekDays.SUNDAY.label
        ]

    def test_delete_with_status_completed(
            self, accessed_manager_account
    ):
        self.data['status'] = CourseStatus.COMPLETED
        course = Course.objects.create(
            **self.data, assigned_by=accessed_manager_account
        )
        with pytest.raises(ValidationError):
            course.delete()

    def test_delete_course_with_enrollment(self, create_enrollment):
        with pytest.raises(ValidationError):
            create_enrollment.course.delete()
