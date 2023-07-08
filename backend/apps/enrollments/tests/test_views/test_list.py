import pytest
from django.urls import reverse
from rest_framework import status
from enrollments.models import Enrollment


@pytest.mark.django_db
class TestEnrollmentListView:
    @pytest.fixture(autouse=True)
    def setup(self, create_enrollment):
        self.enrollment = create_enrollment
        self.url_name = 'enrollments:enrollment_list'
        self.url_path = reverse(self.url_name)

    def test_list_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_by_admin(self, api_client, superuser):
        '''Admin can list all enrollments'''
        api_client.force_authenticate(superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert Enrollment.objects.count() == response.json()['count']

    def test_retrieve_by_manager(self, api_client, manager_account):
        '''Manager can list all enrollments'''
        api_client.force_authenticate(manager_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert Enrollment.objects.count() == response.json()['count']

    def test_retireve_by_student(self, api_client):
        '''Student can list only his enrollments'''
        api_client.force_authenticate(self.enrollment.user)
        response = api_client.get(self.url_path)
        user_enrollments = Enrollment.objects.filter(user=self.enrollment.user)
        assert response.status_code == status.HTTP_200_OK
        assert user_enrollments.count() == response.json()['count']

    def test_retrieve_by_teacher(self, api_client, teacher_account):
        '''Teachers cannot access this page'''
        api_client.force_authenticate(teacher_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_403_FORBIDDEN
