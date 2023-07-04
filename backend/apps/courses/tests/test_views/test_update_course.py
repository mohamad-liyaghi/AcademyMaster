import pytest
from django.urls import reverse
from rest_framework import status
from courses.models import CourseStatus


@pytest.mark.django_db
class TestUpdateCourseView:

    @pytest.fixture(autouse=True)
    def setup(self, create_course):
        self.course = create_course
        self.url_path = reverse(
            'courses:update_course',
            kwargs={'course_token': create_course.token}
        )
        self.data = {
            'price': '123'
        }

    def test_update_unauthorized(self, api_client):
        response = api_client.patch(self.url_path, self.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.patch(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_accessed_manager(
            self, api_client, accessed_manager_account
    ):
        api_client.force_authenticate(accessed_manager_account)
        response = api_client.patch(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_manager_no_perm(self, api_client, manager_account):
        api_client.force_authenticate(manager_account)
        response = api_client.patch(self.url_path, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_completed_course(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        self.course.status = CourseStatus.COMPLETED
        self.course.save()
        response = api_client.patch(self.url_path, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_udpate_running_course(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        self.course.status = CourseStatus.IN_PROGRESS
        self.course.save()
        response = api_client.patch(self.url_path, self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
