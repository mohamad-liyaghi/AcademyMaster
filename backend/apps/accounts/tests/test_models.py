import pytest
from accounts.models import Account, VerificationCode
from datetime import timedelta
from django.utils import timezone


@pytest.fixture
def user():
    return Account.objects.create_user(
        email="simple@simple.com",
        password="1234USERnormal"
    )


@pytest.fixture
def superuser():
    return Account.objects.create_superuser(
        email="superuser@superuser.com",
        password="1234EErrSuperuser"
    )


@pytest.fixture
def manager():
    manager = Account.objects.create_user(
        email="manager@manager.com",
        password="1234USERnormal",
    )
    manager.role = Account.Role.MANAGER
    manager.save()
    return manager


@pytest.fixture
def teacher():
    teacher = Account.objects.create_user(
        email="teacher@teacher.com",
        password="1234USERnormal",
    )
    teacher.role = Account.Role.TEACHER
    teacher.save()
    return teacher


@pytest.mark.django_db
class TestAccountModel:

    def test_user_not_active(self, user):
        assert user.is_active is False

    def test_superuser_is_active(self, superuser):
        assert superuser.is_active is True

    def test_user_has_token(self, user):
        assert user.token is not None

    def test_users_token_is_unique(self, user, superuser):
        assert user.token != superuser.token

    def test_user_is_admin(self, user, superuser):
        assert superuser.is_admin() is True
        assert user.is_admin() is False

    def test_user_is_student(self, user, superuser):
        assert superuser.is_student() is False
        assert user.is_student() is True

    def test_user_is_manager(self, user, superuser, manager):
        assert superuser.is_manager() is False
        assert user.is_manager() is False
        assert manager.is_manager() is True

    def test_user_is_teacher(self, user, superuser, teacher):
        assert superuser.is_teacher() is False
        assert user.is_teacher() is False
        assert teacher.is_teacher() is True


@pytest.mark.django_db
class TestVerificationCodeModel:

    def test_create_verification_code(self, user):
        assert user.verification_codes.count() == 1

    def test_not_create_code_for_superuser(self, superuser):
        assert superuser.verification_codes.count() == 0

    def test_verification_code_is_valid(self, user):
        verification_code = user.verification_codes.first()
        assert verification_code.is_valid() is True

    def test_expired_verification_code(self, user):
        verification_code = user.verification_codes.first()
        verification_code.expire_at = timezone.now() - timedelta(minutes=7)
        verification_code.save()
        assert verification_code.is_valid() is False

    def test_expired_verification_code_by_retry(self, user):
        verification_code = user.verification_codes.first()
        verification_code.retry_count = 5
        verification_code.save()
        assert verification_code.is_valid() is False

    def test_verify_verification_code(self, user):
        verification_code = user.verification_codes.first()
        verified_code = VerificationCode.objects.verify(
            user=user,
            code=verification_code.code
        )
        assert verified_code is True, "Verification code should be valid"

    def test_invalid_verify_verification_code(self, user):
        verification_code = user.verification_codes.first()
        fake_code = int(verification_code.code) + 2
        verified_code = VerificationCode.objects.verify(
            user=user,
            code=fake_code
        )
        assert verified_code is False, "Verification code should not be valid"

    def test_verify_expired_verification_code(self, user):
        verification_code = user.verification_codes.first()
        verification_code.expire_at = verification_code.expire_at - timedelta(minutes=10)
        verification_code.save()
        verified_code = VerificationCode.objects.verify(
            user=user,
            code=verification_code.code
        )
        assert verified_code is False

    def test_verify_verification_code_retry_limit(self, user):
        verification_code = user.verification_codes.first()
        verification_code.retry_count = 5
        verification_code.save()
        verified_code = VerificationCode.objects.verify(
            user=user,
            code=verification_code.code
        )
        assert verified_code is False

    def test_check_or_create(self, user):
        verification_code = user.verification_codes.first()
        verification_code.expire_at = verification_code.expire_at - timedelta(minutes=10)
        verification_code.save()

        check_verification = VerificationCode.objects.check_or_create(user=user)
        assert check_verification is True
        assert user.verification_codes.count() == 2

    def test_check_or_create_valid_token(self, user):
        check_verification = VerificationCode.objects.check_or_create(user=user)
        assert check_verification is False
        assert user.verification_codes.count() == 1
