from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from accounts.utils import generate_unique_verification_code
from accounts.managers import VerificationCodeManager


class VerificationCode(models.Model):
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='verification_codes',
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    retry_count = models.PositiveSmallIntegerField(default=0)

    objects = VerificationCodeManager()

    class Meta:
        db_table = 'verification_codes'
        ordering = ["-created_at"]

    def is_valid(self):
        # Each token is valid for only 5 minuets and can be retried 5 times
        expiration_time = self.created_at + timedelta(minutes=5)
        return expiration_time >= timezone.now() and self.retry < 5

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = generate_unique_verification_code(account=self.account)
        return super().save(*args, **kwargs)
