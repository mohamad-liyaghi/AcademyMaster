import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTeacherListView:
    def setup(self):
        self.url_path = reverse("teachers:teacher_list")

    def test_retrieve_list_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_list(self, api_client, active_account):
        api_client.force_authenticate(active_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_get_list_with_teacher(self, api_client, active_account, teacher_account):
        api_client.force_authenticate(active_account)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] != 0
