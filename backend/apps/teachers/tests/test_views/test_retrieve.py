import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTeacherRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, teacher_account):
        self.teacher = teacher_account
        self.url_path = reverse(
             'teachers:retrieve_teacher',
             kwargs={
                  'teacher_token': self.teacher.teacher.token
                }
            )

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_teacher(self, api_client, active_account):
        api_client.force_authenticate(active_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_invalid_token(
            self, api_client, active_account, unique_uuid
    ):
        api_client.force_authenticate(active_account)
        response = api_client.get(
            reverse(
                'teachers:retrieve_teacher',
                kwargs={'teacher_token': unique_uuid}
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
