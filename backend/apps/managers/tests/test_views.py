from django.urls import reverse
from rest_framework import status
import pytest
from core.tests import user, superuser, api_client, manager
from managers.models import ManagerPermission
from accounts.models import Account

@pytest.mark.django_db    
class TestManagerCreateAPI:

    def setup(self):
        self.create_url = reverse('managers:create_manager')
        self.user = Account.objects.create_user(
            email='manageremail@email.com', password='1234'
        )
        self.data = {
            "user": self.user.id,
            "permissions": []
        }

    def test_unauthorized(self, api_client):
        resp = api_client.post(self.create_url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.user.is_manager()

    def test_promote_superuser(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        self.data['user'] = superuser.id
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_promote_manager_twice(self, api_client, superuser, manager):
        api_client.force_authenticate(superuser)
        self.data['user'] = manager.id
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_promotion_without_permission(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert not self.user.manager.can_promote()

    def test_promotion_with_permission(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        self.data['permissions'] = [*ManagerPermission]
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.user.manager.can_promote()

    def test_insufficient_permission(self, api_client, manager):
        api_client.force_authenticate(manager)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN
