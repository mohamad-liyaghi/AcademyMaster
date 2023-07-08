import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestManagerRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, manager_account):
        self.manager = manager_account
        self.url_name = 'managers:retrieve_manager'
        self.url_path = reverse(
                self.url_name,
                kwargs={'manager_token': self.manager.manager.token}
        )

    def test_retrieve_unauthorized(self, api_client):
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_manager(self, api_client):
        api_client.force_authenticate(self.manager)
        response = api_client.get(self.url_path)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_by_no_manager(self, api_client, active_account):
        '''Only admin/managers can access manager retrieve page'''
        api_client.force_authenticate(active_account)
        assert not active_account.is_manager()
        resp = api_client.get(self.url_path)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_non_existing_manager(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        url_path = reverse(
                self.url_name,
                kwargs={'manager_token': 'invalid_token'}
        )
        resp = api_client.get(url_path)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
