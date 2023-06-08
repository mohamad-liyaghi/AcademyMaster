from django.contrib.auth.models import BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):

    def create_user(self, email: str, password: str, **kwargs):

        email = self.normalize_email(email)

        is_active = False
        user = self.model(
            email=email,
            is_active=is_active,
            role="s",
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
            role="a",
            **kwargs
        )

        user.set_password(password)

        user.save()

        return user


class VerificationCodeManager(models.Manager):

    def verify(self, user, code):

        verification_code = user.verification_codes.first()

        if code == verification_code.code and verification_code.is_valid():
            return True

        verification_code.retry_count += 1
        verification_code.save()
        return False

    def check_or_create(self, user):
        '''Regenerate a token for a user if its token is expired'''
        verification_code = user.verification_codes.first()

        if verification_code and verification_code.is_valid():
            return False

        self.create(account=user)
        return True
