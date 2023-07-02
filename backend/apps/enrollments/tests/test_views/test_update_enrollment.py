import pytest
from django.urls import reverse
from rest_framework import status
from enrollments.models import EnrollmentStatus


@pytest.mark.django_db
class TestEnrollmentUpdateView:
    @pytest.fixture(autouse=True)
    def setup(self, create_enrollment):
        self.enrollment = create_enrollment
        self.url_name = 'enrollments:update_enrollment'
        self.url_path = reverse(
            self.url_name, kwargs={'enrollment_token': self.enrollment.token}
        )
        self.data = {
            'status': EnrollmentStatus.SUCCESS
        }

    def test_update_unauthorized(self, api_client):
        response = api_client.put(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_student(self, api_client):
        api_client.force_authenticate(self.enrollment.user)
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK
        self.enrollment.refresh_from_db()
        assert self.enrollment.status == EnrollmentStatus.SUCCESS

    def test_update_by_manager(self, api_client, manager_account):
        api_client.force_authenticate(manager_account)
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_by_other_student(self, api_client, active_account):
        api_client.force_authenticate(active_account)
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert active_account != self.enrollment.user

    def test_update_by_teacher(self, api_client, teacher_account):
        api_client.force_authenticate(teacher_account)
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_not_found(self, api_client, active_account):
        api_client.force_authenticate(active_account)
        url = reverse(self.url_name, kwargs={'enrollment_token': 'not-found'})
        response = api_client.put(url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_invalid_data(self, api_client):
        api_client.force_authenticate(self.enrollment.user)
        data = {
            'status': 'invalid-status'
        }
        response = api_client.put(self.url_path, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
