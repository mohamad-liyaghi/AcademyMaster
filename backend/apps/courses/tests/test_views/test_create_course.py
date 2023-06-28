import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from core.models import WeekDays
from courses.models import Course, CourseLevel


@pytest.mark.django_db
class TestCreateCourseView:

    @pytest.fixture(autouse=True)
    def setup(self, teacher_account):
        self.data = {
            "title": "test title",
            "description": "test description",
            "location": "test location",
            "instructor": teacher_account.teacher.token,
            "start_date": date(2023, 10, 30),
            "end_date": date(2023, 11, 30),
            "schedule": {},
            "days": [WeekDays.WEDNESDAY.value, WeekDays.FRIDAY.value],
            "session_count": 1,
            "prerequisite": None,
            "level": CourseLevel.A1.value,
            "price": 1000000
        }
        self.url_path = reverse('courses:create_course')

    def test_create_unauthorized(self, api_client):
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.count() == 1

    def test_create_by_accessed_manager(
            self, api_client, accessed_manager_account
    ):
        api_client.force_authenticate(accessed_manager_account)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.count() == 1

    def test_create_by_manager_no_perm(self, api_client, manager_account):
        assert not manager_account.has_perm(
            perm_object=Course.get_permission('add')
        )
        api_client.force_authenticate(manager_account)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_and_set_assigned_by(
            self, api_client, accessed_manager_account
    ):
        api_client.force_authenticate(accessed_manager_account)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.first().assigned_by == accessed_manager_account

    def test_create_by_prerequisite(
            self, api_client, create_course, accessed_manager_account
    ):
        self.data['prerequisite'] = create_course.token

        api_client.force_authenticate(accessed_manager_account)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.last().prerequisite == create_course
