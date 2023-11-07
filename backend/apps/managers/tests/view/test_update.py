import pytest
from django.urls import reverse
from rest_framework import status
from managers.models import Manager


@pytest.mark.django_db
class TestManagerUpdateView:
    @pytest.fixture(autouse=True)
    def setup(self, manager_account):
        self.manager = manager_account
        self.url_name = "managers:update_manager"
        self.url_path = reverse(
            self.url_name, kwargs={"manager_token": self.manager.manager.token}
        )

        self.data = {"permissions": []}

    def test_update_unauthorized_fails(self, api_client):
        resp = api_client.put(self.url_path)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_manager(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        assert not self.manager.has_perm(perm_object=Manager.get_permission("add"))

        # Add permission to perm list
        self.data["permissions"] = [Manager.get_permission("add").codename]

        response = api_client.put(self.url_path, self.data)
        assert self.manager.has_perm(perm_object=Manager.get_permission("add"))
        assert response.status_code == status.HTTP_200_OK

    def test_update_remove_all_perms(self, api_client, superuser):
        """When parsing perm list empty, all user perms would be deleted"""
        api_client.force_authenticate(superuser)
        # Empty perm list
        self.data["permissions"] = []
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK
        assert self.manager.user_permissions.count() == 0

    def test_update_permission_denied(self, api_client):
        """
        Only manager with managers.change_manager
        can update other managers
        """
        api_client.force_authenticate(self.manager)
        assert not self.manager.has_perm(perm_object=Manager.get_permission("change"))
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_by_accessed_manager(self, api_client, accessed_manager_account):
        """
        Manager with managers.change_manager can update others
        """
        api_client.force_authenticate(accessed_manager_account)
        assert accessed_manager_account.has_perm(
            perm_object=Manager.get_permission("change")
        )
        response = api_client.put(self.url_path, self.data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_non_exist_manager(self, api_client, superuser, unique_uuid):
        api_client.force_authenticate(superuser)
        url = reverse(self.url_name, kwargs={"manager_token": unique_uuid})
        response = api_client.put(url, self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
