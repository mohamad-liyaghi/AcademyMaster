import pytest
from django.urls import reverse
from rest_framework import status
from teachers.models import Teacher


@pytest.mark.django_db
class TestRetrieveActivityView:
    @pytest.fixture(autouse=True)
    def setup(self, get_activity):
        self.activity = get_activity
        self.url_name = "activities:activity_list"
        self.url_path = reverse(
            self.url_name, kwargs={"course_token": get_activity.course.token}
        )

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_by_admin(self, api_client, superuser):
        api_client.force_authenticate(user=superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_manager(self, api_client, manager_account):
        api_client.force_authenticate(user=manager_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_course_instructor(self, api_client):
        api_client.force_authenticate(self.activity.course.instructor.user)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_other_teacher(
        self, api_client, teacher_account, active_account
    ):
        """Only the course instructor can retrieve activities of a course"""

        # Change the instructor
        self.activity.course.instructor = Teacher.objects.create(user=active_account)
        self.activity.course.save()

        api_client.force_authenticate(user=teacher_account)
        response = api_client.get(self.url_path)

        assert teacher_account != self.activity.course.instructor.user
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_by_student(self, api_client, active_account):
        api_client.force_authenticate(user=active_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_invalid_course_token(self, api_client, superuser, unique_uuid):
        assert unique_uuid != self.activity.course.token
        self.url_path = reverse(self.url_name, kwargs={"course_token": unique_uuid})
        api_client.force_authenticate(user=superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_404_NOT_FOUND
