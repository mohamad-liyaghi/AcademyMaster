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

    def verify_verification_code(self, user, code):
        verification_code = self.get_queryset().filter(account=user).first()

        if code == verification_code.code and verification_code.retry_count < 5:
            return True

        verification_code.retry_count += 1
        verification_code.save()
        return False
