import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from managers.models import Manager
from core.tests import user, superuser, manager, teacher


@pytest.mark.django_db
class TestManagerModel:


    def test_promote_manager(self, user):
        Manager.objects.create(user=user)
        assert user.is_manager()

    def test_duplicate_promote_manager(self, manager):
        with pytest.raises(IntegrityError):
            Manager.objects.create(user=manager)

    def test_promote_manager_no_permission(self, manager, user):
        assert not manager.has_perm(perm_object=Manager.get_permission('add'))
        with pytest.raises(ValidationError):
            Manager.objects.create(user=manager, promoted_by=user)

    def test_promote_manager_with_permission(self, user):
        manager_user = get_user_model().objects.create_superuser(
            email='another@fake.com',
            password='1234EErr'
        )

        manager = Manager.objects.create_with_permissions(
            user=manager_user,
            permissions=[
                Manager.get_permission('add')
            ]
        )

        assert manager_user.has_perm(perm_object=Manager.get_permission('add'))

        Manager.objects.create(user=user, promoted_by=manager_user)
        assert user.manager.promoted_by == manager_user

    def test_promote_manager_by_admin(self, superuser, user):

        Manager.objects.create(user=user, promoted_by=superuser)
        assert user.manager.promoted_by == superuser

    def test_remove_permission(self, manager):
        manager.user_permissions.add(Manager.get_permission('add'))
        assert manager.has_perm(perm_object=Manager.get_permission('add'))

        manager.user_permissions.remove(
            Manager.get_permission('add')
        )
        assert not manager.has_perm(perm_object=Manager.get_permission('add'))

    def test_remove_permission_after_deletion(self, manager):
        manager.user_permissions.add(
            Manager.get_permission('add')
        )
        manager = get_object_or_404(get_user_model(), id=manager.id)
        assert manager.has_perm(perm_object=Manager.get_permission('add'))

        Manager.objects.get(user=manager).delete()

        assert not manager.has_perm(perm_object=Manager.get_permission('add'))

    def test_create_manager_with_permission(self, user):
        user.is_active = True
        user.save()

        Manager.objects.create_with_permissions(
            user=user,
            permissions=[
                Manager.get_permission('add')
            ]
        )
        assert user.has_perm(perm_object=Manager.get_permission('add'))
        user_id = user.id
        user = get_object_or_404(get_user_model(), id=user_id)
        assert user.has_perm(perm_object=Manager.get_permission('add'))
