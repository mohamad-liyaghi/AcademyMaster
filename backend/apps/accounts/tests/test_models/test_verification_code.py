import pytest
from datetime import timedelta
from django.utils import timezone
from accounts.models import VerificationCode
from accounts.models.exceptions import (
    DuplicationCodeException,
    ActiveUserCodeException
)


@pytest.mark.django_db
class TestVerificationCodeModel:

    def test_verification_code_is_not_expired(self, deactive_account):
        assert not deactive_account.verification_codes.first().is_expired()

    def test_verification_code_is_expired(self, deactive_account):
        verification_code = deactive_account.verification_codes.first()
        verification_code.expire_at = timezone.now() - timedelta(minutes=7)
        verification_code.save()
        assert verification_code.is_expired()

    def test_verify_verification_code(self, deactive_account):
        verification_code = deactive_account.verification_codes.first()
        verified_code = VerificationCode.objects.verify(
            user=deactive_account,
            code=verification_code.code
        )
        assert verified_code[0]

    def test_verify_invalid_code(self, deactive_account):
        verification_code = deactive_account.verification_codes.first()
        fake_code = int(verification_code.code) + 2
        assert verification_code.code != fake_code
        verified_code = VerificationCode.objects.verify(
            user=deactive_account,
            code=fake_code
        )
        assert not verified_code[0]

    def test_verify_expired_verification_code(self, deactive_account):
        verification_code = deactive_account.verification_codes.first()
        verification_code.expire_at = (
            verification_code.expire_at - timedelta(minutes=10)
        )
        verification_code.save()

        assert verification_code.is_expired()
        verified_code = VerificationCode.objects.verify(
            user=deactive_account,
            code=verification_code.code
        )
        assert not verified_code[0]

    def test_verify_code_retry_limit(self, deactive_account):
        '''Codes that has been retried for 5 times, are invalid'''
        verification_code = deactive_account.verification_codes.first()
        verification_code.retry_count = 5
        verification_code.save()
        verified_code = VerificationCode.objects.verify(
            user=deactive_account,
            code=verification_code.code
        )
        assert not verified_code[0]

    def test_create_verification_code_twice(self, deactive_account):
        verification_code = deactive_account.verification_codes.first()

        assert not verification_code.is_expired()
        with pytest.raises(DuplicationCodeException):
            VerificationCode.objects.create(user=deactive_account)

    def test_create_verification_for_active_user(self, active_account):
        assert active_account.is_active
        with pytest.raises(ActiveUserCodeException):
            VerificationCode.objects.create(user=active_account)
