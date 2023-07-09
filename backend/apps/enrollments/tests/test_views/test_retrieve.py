import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestEnrollmentRetrieveView:
    @pytest.fixture(autouse=True)
    def setup(self, create_enrollment):
        self.enrollment = create_enrollment
        self.url_name = 'enrollments:retrieve_enrollment'
        self.url_path = reverse(
            self.url_name, kwargs={'enrollment_token': self.enrollment.token}
        )

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_manager(self, api_client, accessed_manager_account):
        api_client.force_authenticate(accessed_manager_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_enrollment_user(self, api_client):
        '''Test that enrollment user can retrieve his enrollment.'''
        user = self.enrollment.user
        api_client.force_authenticate(user)
        assert user == self.enrollment.user
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_other_student(self, api_client, active_account):
        '''Test that other student can't retrieve enrollment.'''
        api_client.force_authenticate(active_account)
        assert active_account != self.enrollment.user
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_by_teacher(self, api_client, teacher_account):
        '''Test that teacher can't retrieve enrollment.'''
        api_client.force_authenticate(teacher_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_not_existing_enrollment(
            self, api_client, superuser, unique_uuid
    ):
        api_client.force_authenticate(superuser)
        url_path = reverse(
            self.url_name, kwargs={'enrollment_token': unique_uuid}
        )
        response = api_client.get(url_path)
        assert response.status_code == status.HTTP_404_NOT_FOUND
