from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from accounts.models import VerificationCode
from apps.core.tasks import send_email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_verification_code(sender, created, instance, **kwargs):
    if created:
        if not instance.is_superuser:
            VerificationCode.objects.create(account=instance)


@receiver(post_save, sender=VerificationCode)
def send_verification_email(sender, created, instance, **kwargs):
    if created:
        verification_code = instance
        account = verification_code.account

        send_email.delay(
            template_path="emails/verification_code.html",
            to_email=account.email,
            subject='Verify Your Account',
            context={
                'verification_code': verification_code.code,
                'first_name': account.first_name,
                'expire_at': verification_code.expire_at,
            }
        )
