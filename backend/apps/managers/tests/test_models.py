import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from managers.models import Manager, ManagerPermission
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
        assert not Manager.objects.has_permission(
            user=manager,
            permission=ManagerPermission.PROMOTE.value
        )
        with pytest.raises(ValidationError):
            Manager.objects.create(user=manager, promoted_by=user)

    def test_promote_manager_with_permission(self, manager, user):
        assert not Manager.objects.has_permission(
            user=manager,
            permission=ManagerPermission.PROMOTE.value
        )

        # Give related permissions to the user
        Manager.objects.add_permissions(
            user=manager,
            permissions=[
                ManagerPermission.PROMOTE,
            ]
        )
        assert Manager.objects.has_permission(
            user=manager,
            permission=ManagerPermission.PROMOTE.value
        )
        Manager.objects.create(user=user, promoted_by=manager)
        assert user.manager.promoted_by == manager

    def test_promote_manager_by_admin(self, superuser, user):

        Manager.objects.create(user=user, promoted_by=superuser)
        assert user.manager.promoted_by == superuser

    def test_remove_permission(self, manager):
        Manager.objects.add_permissions(
            permissions=[
                ManagerPermission.PROMOTE,
            ],
            user=manager,
        )
        assert Manager.objects.has_permission(
            user=manager,
            permission=ManagerPermission.PROMOTE.value
        )

        Manager.objects.remove_permissions(
            user=manager,
            permissions=[
                ManagerPermission.PROMOTE,
            ]
        )
        assert not Manager.objects.has_permission(
            user=manager,
            permission=ManagerPermission.PROMOTE.value
        )

    def test_remove_permission_after_deletion(self, manager):
        Manager.objects.add_permissions(
            user=manager,
            permissions=[
                ManagerPermission.PROMOTE,
            ]
        )
        assert Manager.objects.has_permission(
            user=manager,
            permission=ManagerPermission.PROMOTE.value
        )

        Manager.objects.get(user=manager).delete()

        assert not manager.user_permissions.filter(
            codename=ManagerPermission.PROMOTE.value
        ).exists()

    def test_create_manager_with_permission(self, user):
        user.is_active = True
        user.save()
        manager = Manager.objects.create_with_permissions(
            user=user,
            permissions=[
                ManagerPermission.PROMOTE
            ]
        )
        assert Manager.objects.has_permission(
            user=user,
            permission=ManagerPermission.PROMOTE.value
        )
