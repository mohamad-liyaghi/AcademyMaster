import pytest
from django.urls import reverse
from rest_framework import status
from managers.models import Manager


@pytest.mark.django_db
class TestManagerCreateView:
    @pytest.fixture(autouse=True)
    def setup(self, active_account):
        self.url_path = reverse("managers:create_manager")
        self.user = active_account
        self.data = {"user": self.user.token, "permissions": []}

    def test_create_unauthorized(self, api_client):
        response = api_client.post(self.url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_without_manager_perm(self, api_client, superuser):
        """Promote a manager with empty permissions"""
        api_client.force_authenticate(superuser)
        response = api_client.post(self.url_path, self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.user.is_manager()
        assert not self.user.has_perm(perm_object=Manager.get_permission("add"))

    def test_promote_with_manager(self, api_client, superuser):
        """Promote manager with permissions"""
        api_client.force_authenticate(superuser)
        self.data["permissions"] = [Manager.get_permission("add").codename]
        resp = api_client.post(self.url_path, self.data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.user.has_perm(perm_object=Manager.get_permission("add"))

    def test_promote_superuser(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        self.data["user"] = superuser.token
        resp = api_client.post(self.url_path, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_promote_manager_twice(self, api_client, superuser, manager_account):
        api_client.force_authenticate(superuser)
        self.data["user"] = manager_account.id
        resp = api_client.post(self.url_path, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_without_promoter_permission(self, api_client, manager_account):
        """Managers with managers.add_manager perm can only add managers"""
        api_client.force_authenticate(manager_account)
        resp = api_client.post(self.url_path, self.data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_create_with_promoter_permission(
        self, api_client, accessed_manager_account
    ):
        assert accessed_manager_account.has_perm(
            perm_object=Manager.get_permission("add")
        )
        api_client.force_authenticate(accessed_manager_account)
        resp = api_client.post(self.url_path, self.data)
        assert resp.status_code == status.HTTP_201_CREATED
