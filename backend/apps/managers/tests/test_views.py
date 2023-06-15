from django.urls import reverse
from rest_framework import status
import pytest
from core.tests import user, superuser, api_client, manager
from managers.models import ManagerPermission, Manager
from accounts.models import Account


@pytest.mark.django_db
class TestManagerCreateView:

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


@pytest.mark.django_db
class TestManagerUpdateView:
    def setup(self):
        self.data = {
            "permissions": []
        }

    def test_update_manager_unauthorized(self, api_client, manager):
        resp = api_client.put(
            reverse(
                'managers:update_manager',
                kwargs={'manager_token': manager.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_manager(self, api_client, manager, superuser):
        api_client.force_authenticate(superuser)
        self.data['permissions'] = [ManagerPermission.PROMOTE]
        assert not manager.manager.can_promote()
        resp = api_client.put(
            reverse(
                'managers:update_manager',
                kwargs={'manager_token': manager.manager.token},
            ),
            self.data
        )
        assert manager.manager.can_promote()
        assert resp.status_code == status.HTTP_200_OK

    def test_update_manager_remove_permissions(self, api_client, manager, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.put(
            reverse(
                'managers:update_manager',
                kwargs={'manager_token': manager.manager.token},
            ),
            self.data
        )
        assert resp.status_code == status.HTTP_200_OK
        assert not manager.user_permissions.all()

    def test_update_user_no_permission(self, api_client, manager, superuser):
        '''Only admins and promoter can update a manager'''
        api_client.force_authenticate(manager)
        resp = api_client.put(
            reverse(
                'managers:update_manager',
                kwargs={'manager_token': manager.manager.token},
            ),
            self.data
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_update_user_remove_and_add(self, api_client, manager, superuser):
        api_client.force_authenticate(superuser)
        Manager.objects.add_permissions(manager, [ManagerPermission.DEMOTE])
        assert manager.manager.can_demote()
        assert not manager.manager.can_promote()

        self.data['permissions'] = [ManagerPermission.PROMOTE]
        resp = api_client.put(
            reverse(
                'managers:update_manager',
                kwargs={'manager_token': manager.manager.token},
            ),
            self.data
        )
        assert resp.status_code == status.HTTP_200_OK
        assert not manager.manager.can_demote()
        assert manager.manager.can_promote()


@pytest.mark.django_db
class TestManagerDeleteView:
    def test_delete_unauthorized(self, api_client, manager):
        resp = api_client.delete(
            reverse(
                'managers:delete_manager',
                kwargs={'manager_token': manager.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_by_admin(self, api_client, manager, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.delete(
            reverse(
                'managers:delete_manager',
                kwargs={'manager_token': manager.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_manager(self, api_client, manager, user):
        user.is_active = True
        user.save()
        Manager.objects.create(user=user)
        assert user.is_manager()

        api_client.force_authenticate(manager)
        Manager.objects.add_permissions(
            manager,
            [ManagerPermission.DEMOTE]
        )
        assert manager.manager.can_demote()
        resp = api_client.delete(
            reverse(
                'managers:delete_manager',
                kwargs={'manager_token': user.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_manager_without_permission(self, api_client, manager, user):
        user.is_active = True
        user.save()
        Manager.objects.create(user=user)
        assert user.is_manager()

        api_client.force_authenticate(manager)
        assert not manager.manager.can_demote()
        resp = api_client.delete(
            reverse(
                'managers:delete_manager',
                kwargs={'manager_token': user.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestManagerRetrieveView:
    def test_retrieve_unauthorized(self, api_client, manager):
        resp = api_client.get(
            reverse(
                'managers:retrieve_manager',
                kwargs={'manager_token': manager.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve(self, api_client, manager, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.get(
            reverse(
                'managers:retrieve_manager',
                kwargs={'manager_token': manager.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_200_OK

    def test_retrieve_access_denied(self, api_client, manager, user):
        api_client.force_authenticate(user)
        resp = api_client.get(
            reverse(
                'managers:retrieve_manager',
                kwargs={'manager_token': manager.manager.token}
            )
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestManagerListView:
    def test_retrieve_list_unauthorized(self, api_client):
        resp = api_client.get(
            reverse(
                'managers:manager_list',
            )
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_list(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.get(reverse('managers:manager_list',))
        assert resp.status_code == status.HTTP_200_OK
    
    def test_retrieve_list_access_denied(self, api_client, user):
        api_client.force_authenticate(user)
        resp = api_client.get(reverse('managers:manager_list'))
        assert resp.status_code == status.HTTP_403_FORBIDDEN
