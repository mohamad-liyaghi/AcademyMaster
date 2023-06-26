import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTeacherUpdateView:
    @pytest.fixture(autouse=True)
    def setup(self, teacher_account):
        self.teacher = teacher_account
        self.url_name = 'teachers:update_teacher'
        self.url_path = reverse(
            self.url_name,
            kwargs={'teacher_token': self.teacher.teacher.token}
        )

    def test_update_unauthorized(self, api_client):
        response = api_client.put(self.url_path, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_by_object_owner(self, api_client):
        updated_description = 'Updated description'
        api_client.force_authenticate(self.teacher)
        response = api_client.put(
            self.url_path,
            {'description': updated_description}
        )
        assert response.status_code == status.HTTP_200_OK
        self.teacher.teacher.refresh_from_db()
        assert self.teacher.teacher.description == updated_description

    def test_update_other_teachers(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.put(self.url_path, {})
        assert not superuser == self.teacher.teacher.user
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_invalid_teacher(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.put(
            reverse(
                self.url_name,
                kwargs={'teacher_token': 'Invalid Token'}
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
