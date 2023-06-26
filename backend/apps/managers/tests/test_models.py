import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from managers.models import Manager


@pytest.mark.django_db
class TestManagerModel:
    def test_create_manager(self, active_account):
        Manager.objects.create(user=active_account)
        assert active_account.is_manager()

    def test_duplicate_create_manager(self, manager_account):
        '''A user can only once promote as manager'''
        with pytest.raises(IntegrityError):
            Manager.objects.create(user=manager_account)

    def test_promote_by_non_accessed(self, manager_account, active_account):
        '''Only Admin/Manager with add_manager perm can promote'''
        assert not manager_account.has_perm(
            perm_object=Manager.get_permission('add')
        )
        with pytest.raises(ValidationError):
            Manager.objects.create(
                user=active_account, promoted_by=manager_account
            )

    def test_prmote_by_accessed_manager(
            self, active_account, accessed_manager_account
    ):
        assert accessed_manager_account.has_perm(
            perm_object=Manager.get_permission('add')
        )

        Manager.objects.create(
            user=active_account,
            promoted_by=accessed_manager_account
        )
        assert active_account.is_manager()
        assert active_account.manager.promoted_by == accessed_manager_account

    def test_promote_manager_by_admin(self, superuser, active_account):

        Manager.objects.create(
            user=active_account, promoted_by=superuser
        )
        assert active_account.is_manager()
        assert active_account.manager.promoted_by == superuser

    def test_remove_permission(self, manager_account):
        manager_account.user_permissions.add(Manager.get_permission('add'))
        assert manager_account.has_perm(
            perm_object=Manager.get_permission('add')
        )

        manager_account.user_permissions.remove(
            Manager.get_permission('add')
        )
        assert not manager_account.has_perm(
            perm_object=Manager.get_permission('add')
        )

    def test_remove_permission_after_deletion(self, accessed_manager_account):
        '''Remove a user permissoin when its manager instance gets deleted'''
        assert accessed_manager_account.has_perm(
            perm_object=Manager.get_permission('add')
        )

        Manager.objects.get(user=accessed_manager_account).delete()

        assert not accessed_manager_account.has_perm(
            perm_object=Manager.get_permission('add')
        )

    def test_create_manager_with_permission(self, active_account):
        Manager.objects.create_with_permissions(
            user=active_account,
            permissions=[
                Manager.get_permission('add')
            ]
        )
        assert active_account.has_perm(
            perm_object=Manager.get_permission('add')
        )
        assert active_account.has_perm(
            perm_object=Manager.get_permission('add')
        )
