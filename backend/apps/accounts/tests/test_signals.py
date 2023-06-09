import pytest
from core.tests import user, superuser


@pytest.mark.django_db
class TestVerificationSignal:
    def test_create_verification_for_user(self, user):
        assert user.verification_codes.count() == 1

    def test_dont_create_verification_for_superuser(self, superuser):
        assert superuser.verification_codes.count() == 0
