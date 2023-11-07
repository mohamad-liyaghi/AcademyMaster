import pytest


@pytest.mark.django_db
class TestVerificationCodeSignal:
    def test_code_is_created_for_inactive_user(self, inactive_account):
        """
        This signal should create a verification code for an inactive user when its created
        """
        assert inactive_account.verification_codes.count() == 1

    def test_code_is_not_created_for_superuser(self, superuser):
        assert superuser.verification_codes.count() == 0
