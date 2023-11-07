import pytest
from django.urls import reverse
from rest_framework import status
from managers.models import Manager


@pytest.mark.django_db
class TestManagerListView:
    def setup(self):
        self.url_path = reverse("managers:manager_list")

    def test_retrieve_list_unauthorized(self, api_client):
        resp = api_client.get(self.url_path)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.get(self.url_path)
        assert resp.status_code == status.HTTP_200_OK

    def test_list_by_manager(self, api_client, manager_account):
        api_client.force_authenticate(manager_account)
        resp = api_client.get(self.url_path)
        assert resp.status_code == status.HTTP_200_OK

    def test_list_non_manager(self, api_client, active_account):
        """Non managers cant access manager list page"""
        api_client.force_authenticate(active_account)
        resp = api_client.get(self.url_path)
        assert resp.status_code == status.HTTP_403_FORBIDDEN
