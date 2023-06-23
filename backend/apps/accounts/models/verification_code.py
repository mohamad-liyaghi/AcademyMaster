from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
from accounts.utils import generate_unique_verification_code
from accounts.managers import VerificationCodeManager


class VerificationCode(models.Model):
    account = models.ForeignKey(
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
        return not self.expire_at >= datetime.now(pytz.timezone('Asia/Tehran'))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = generate_unique_verification_code(account=self.account)
            self.expire_at = timezone.now() + timedelta(minutes=5)

        return super().save(*args, **kwargs)
