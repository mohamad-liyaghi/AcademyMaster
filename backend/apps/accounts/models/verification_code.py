from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
from accounts.utils import generate_unique_verification_code
from accounts.managers import VerificationCodeManager
tehran_tz = pytz.timezone('Asia/Tehran')


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

    def is_valid(self):
        if self.retry_count >= 5:
            return False

        return self.expire_at >= datetime.now(tehran_tz)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = generate_unique_verification_code(account=self.account)
            self.expire_at = timezone.now() + timedelta(minutes=5)

        return super().save(*args, **kwargs)
