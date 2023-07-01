import pytest
from django.urls import reverse
from rest_framework import status
from enrollments.models import EnrollmentStatus


@pytest.mark.django_db
class TestCreateEnrollmentView:

    @pytest.fixture(autouse=True)
    def setup(self, create_course):
        self.data = {
            'course': create_course.token,
        }
        self.url_path = reverse('enrollments:create_enrollment')

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
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_by_manager(self, api_client, manager_account):
        api_client.force_authenticate(manager_account)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_by_teacher(self, api_client, teacher_account):
        api_client.force_authenticate(teacher_account)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_by_student(self, api_client, active_account):
        api_client.force_authenticate(active_account)
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['course'] == self.data['course']
        assert response.data['user'] == active_account.full_name
        assert response.data['status'] == EnrollmentStatus.PENDING

    def test_create_twice_pending_enrollment(self, api_client, active_account):
        '''Test raise err if user has already a pending enrollment'''
        api_client.force_authenticate(active_account)
        api_client.post(
            self.url_path, self.data, format='json'
        )
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_already_enrolled(
            self, api_client, create_enrollment
    ):
        '''Test raise error if user has already enrolled'''
        active_account = create_enrollment.user
        create_enrollment.status = EnrollmentStatus.SUCCESS
        create_enrollment.save()
        create_enrollment.refresh_from_db()

        api_client.force_authenticate(active_account)
        self.data['course'] = create_enrollment.course.token
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_already_failed(
            self, api_client, active_account, create_enrollment
    ):
        '''Test that a student can enroll even if there is a failed enroll'''
        create_enrollment.status = EnrollmentStatus.FAILED
        create_enrollment.save()

        api_client.force_authenticate(active_account)
        self.data['course'] = create_enrollment.course.token
        response = api_client.post(
            self.url_path, self.data, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['course'] == self.data['course']
        assert response.data['user'] == active_account.full_name
        assert response.data['status'] == EnrollmentStatus.PENDING
