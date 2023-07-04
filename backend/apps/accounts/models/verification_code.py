from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from accounts.models.exceptions import (
    DuplicationCodeException,
    ActiveUserCodeException
)
from accounts.utils import generate_unique_verification_code
from accounts.managers import VerificationCodeManager


class VerificationCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='verification_codes',
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=5)
    expire_at = models.DateTimeField()
    retry_count = models.PositiveSmallIntegerField(default=0)

    objects = VerificationCodeManager()

    class Meta:
        db_table = 'verification_codes'
        ordering = ["expire_at"]

    def is_expired(self):
        '''Check if the code is expired'''
        return not self.expire_at >= timezone.now()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.__check_user_not_active()
            self.__check_code_not_exist()
            self.code = generate_unique_verification_code(user=self.user)
            self.expire_at = timezone.now() + timedelta(minutes=5)

        return super().save(*args, **kwargs)

    def __check_code_not_exist(self):
        '''Raise error if an active code already exists for user'''
        verification_code = self.user.verification_codes.first()

        if verification_code and not verification_code.is_expired():
            raise DuplicationCodeException('An active code already exists')

        return

    def __check_user_not_active(self):
        if self.user.is_active:
            raise ActiveUserCodeException("User is already active")

        return
