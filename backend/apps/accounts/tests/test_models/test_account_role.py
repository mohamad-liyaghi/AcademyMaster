import pytest


@pytest.mark.django_db
class TestAccountRoleModel:
    def test_user_is_admin(self, superuser, active_account):
        '''Superusers are admin'''
        assert superuser.is_admin()
        assert not active_account.is_admin()

    def test_user_is_manager(self, active_account, superuser, manager_account):
        '''Admins and accounts with manager object are managers'''
        assert superuser.is_manager()
        assert manager_account.is_manager()
        assert not active_account.is_manager()

    def test_user_is_teacher(self, superuser, teacher_account, active_account):
        assert superuser.is_teacher()
        assert teacher_account.is_teacher()
        assert not active_account.is_teacher()

    def test_user_is_student(self, superuser, active_account, teacher_account):
        '''Users who are not teacher/admin/manager are all students'''
        assert not superuser.is_student()
        assert active_account.is_student()
        assert not teacher_account.is_student()
