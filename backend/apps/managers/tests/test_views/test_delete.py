import pytest
from django.urls import reverse
from rest_framework import status
from managers.models import Manager


@pytest.mark.django_db
class TestManagerDeleteView:

    @pytest.fixture(autouse=True)
    def setup(self, manager_account):
        self.manager = manager_account
        self.url_name = 'managers:delete_manager'
        self.url_path = reverse(
                self.url_name,
                kwargs={'manager_token': self.manager.manager.token}
            )

    def test_delete_unauthorized(self, api_client):
        resp = api_client.delete(self.url_path)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_admin(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.delete(self.url_path)
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_accessed_manager(
            self, api_client, accessed_manager_account
    ):
        '''
        Manager with managers.delete_manager perm can delete other managres
        '''

        assert accessed_manager_account.is_manager()
        assert accessed_manager_account.has_perm(
            perm_object=Manager.get_permission('delete')
        )

        api_client.force_authenticate(accessed_manager_account)

        response = api_client.delete(self.url_path)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_manager_without_permission(self, api_client):
        api_client.force_authenticate(self.manager)
        assert not self.manager.has_perm(
            perm_object=Manager.get_permission('delete')
        )
        resp = api_client.delete(self.url_path)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_non_existing_manager(
            self, api_client, superuser, unique_uuid
    ):
        api_client.force_authenticate(superuser)
        url_path = reverse(
                self.url_name,
                kwargs={'manager_token': unique_uuid}
            )
        resp = api_client.delete(url_path)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
