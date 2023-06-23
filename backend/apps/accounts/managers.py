from django.contrib.auth.models import BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):

    def create_user(self, email: str, password: str, **kwargs):

        email = self.normalize_email(email)

        is_active = False
        user = self.model(
            email=email,
            is_active=is_active,
            **kwargs
        )

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_active=True,
            is_superuser=True,
            **kwargs
        )

        user.set_password(password)

        user.save()

        return user


class VerificationCodeManager(models.Manager):

    def verify(self, user, code: str) -> bool:
        '''
        Verify a verification code
        '''
        verification_code = user.verification_codes.first()

        if not verification_code:
            return False, "No verification code found"

        if verification_code.is_expired():
            return False, 'Code is Expired.'

        if verification_code.code == code:
            if verification_code.retry_count >= 5:
                return (False, f'Maximum retry exceeded, \
                        wait until {verification_code.expire_at}')
            # If code is valid and retries are less than 5
            return True, 'Code is valid'

        # code is incorrect, update retry count
        verification_code.retry_count += 1
        verification_code.save()
        return False, "Invalid code"

    def re_generate(self, user) -> bool:
        '''Re generate verification code if verification code is expired'''
        verification_code = user.verification_codes.first()

        if not verification_code or verification_code.is_expired():
            self.create(account=user)
            return True

        return False
