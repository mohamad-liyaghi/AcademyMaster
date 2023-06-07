import pytest
from accounts.models import Account

@pytest.mark.django_db
class TestAccountModel:

    def setup(self):
        self.user = Account.objects.create_user(
            email="simple@simple.com",
            password="1234USERnormal"
        )

        self.superuser = Account.objects.create_superuser(
            email="superuser@superuser.com",
            password="1234EErrSuperuser"
        )

    def test_user_not_active(self):
        assert self.user.is_active == False

    def test_superuser_is_active(self):
        assert self.superuser.is_active == True

    def test_user_has_token(self):
        assert self.user.token is not None

    def test_users_token_is_unique(self):
        assert self.user.token != self.superuser.token

    def test_user_is_admin(self):
        assert self.superuser.is_admin() == True
        assert self.user.is_admin() == False

    def test_user_is_student(self):
        assert self.superuser.is_student() == False
        assert self.user.is_student() == True

    def test_user_is_manager(self):
        manager = Account.objects.create_user(
            email="manager@manager.com",
            password="1234USERnormal",
        )
        manager.role = Account.Role.MANAGER
        manager.save()
        assert self.superuser.is_manager() == False
        assert self.superuser.is_manager() == False
        assert manager.is_manager() == True

    def test_user_is_teacher(self):
        teacher = Account.objects.create_user(
            email="teacher@teacher.com",
            password="1234USERnormal",
        )
        teacher.role = Account.Role.TEACHER
        teacher.save()
        assert self.superuser.is_teacher() == False
        assert self.superuser.is_teacher() == False
        assert teacher.is_teacher() == True