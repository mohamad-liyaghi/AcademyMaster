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
        assert not manager.manager.can_promote()
        with pytest.raises(ValidationError):
            Manager.objects.create(user=manager, promoted_by=user)

    def test_promote_manager_with_permission(self, manager, user):
        assert not manager.manager.can_promote()

        # Give related permissions to the user
        Manager.objects.add_permissions(
            user=manager,
            codenames=[
                ManagerPermission.PROMOTE.value,
            ]
        )
        assert manager.manager.can_promote()
        Manager.objects.create(user=user, promoted_by=manager)
        assert user.manager.promoted_by == manager

    def test_remove_permission(self, manager):
        Manager.objects.add_permissions(
            user=manager,
            codenames=[
                ManagerPermission.PROMOTE.value,
            ]
        )
        assert manager.manager.can_promote()

        Manager.objects.remove_permissions(
            user=manager,
            codenames=[
                ManagerPermission.PROMOTE.value,
            ]
        )
        assert not manager.manager.can_promote()

    def test_remove_permission_after_deletion(self, manager):
        Manager.objects.add_permissions(
            user=manager,
            codenames=[
                ManagerPermission.PROMOTE.value,
            ]
        )
        assert manager.manager.can_promote()

        Manager.objects.get(user=manager).delete()

        assert not manager.user_permissions.filter(
            codename=ManagerPermission.PROMOTE.value
        ).exists()
