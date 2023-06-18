from django.urls import reverse
from rest_framework import status
import pytest
from core.tests import user, superuser, api_client, manager
from managers.models import Manager
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
        assert not self.user.has_perm(Manager.get_permission('add'))

    def test_promotion_with_permission(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        self.data['permissions'] = [Manager.get_permission('add')]
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.user.user_permissions.filter(
            codename=Manager.get_permission('add').codename
        ).exists()

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
        self.data['permissions'] = [
            Manager.get_permission('add')
        ]
        assert not manager.user_permissions.filter(
            codename=Manager.get_permission('add').codename
        ).exists()
        resp = api_client.put(
            reverse(
                'managers:update_manager',
                kwargs={'manager_token': manager.manager.token},
            ),
            self.data
        )
        assert manager.user_permissions.filter(
            codename=Manager.get_permission('add').codename
        ).exists()
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

    def test_update_user_remove_and_add(self, api_client, superuser, user):
        user.is_active = True
        user.save()
        api_client.force_authenticate(superuser)
        Manager.objects.create_with_permissions(
            permissions=[Manager.get_permission('delete')],
            user=user
        )
        assert user.has_perm(
            Manager.get_permission('delete', return_str=True)
        )
        assert not user.has_perm(
            Manager.get_permission('add', return_str=True)
        )

        self.data['permissions'] = [Manager.get_permission('add')]
        resp = api_client.put(
            reverse(
                'managers:update_manager',
                kwargs={'manager_token': user.manager.token},
            ),
            self.data
        )
        assert resp.status_code == status.HTTP_200_OK
        assert not user.user_permissions.filter(
            codename=Manager.get_permission('delete').codename
        ).exists()
        assert user.user_permissions.filter(
            codename=Manager.get_permission('add').codename
        ).exists()


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
        DELETE_PERMISSION = Manager.get_permission('delete')
        Manager.objects.create_with_permissions(
            user=user,
            permissions=[
                DELETE_PERMISSION,
            ]
        )
        assert user.is_manager()
        assert user.has_perm(
            Manager.get_permission('delete', return_str=True)
        )

        # Add delete permission for user
        manager.user_permissions.add(
            DELETE_PERMISSION
        )

        api_client.force_authenticate(user)

        resp = api_client.delete(
            reverse(
                'managers:delete_manager',
                kwargs={'manager_token': manager.manager.token}
            )
        )

        assert resp.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_by_manager_without_permission(self, api_client, manager, user):
        user.is_active = True
        user.save()
        Manager.objects.create(user=user)
        assert user.is_manager()

        api_client.force_authenticate(manager)
        assert not manager.has_perm(Manager.get_permission('delete'))
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
