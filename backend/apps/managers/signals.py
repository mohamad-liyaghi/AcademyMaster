from django.dispatch import receiver
from django.db.models.signals import post_save

from managers.models import Manager
from apps.core.tasks import send_email


@receiver(post_save, sender=Manager)
def send_promotion_email(sender, created, instance, **kwargs):
    if created:
        manager = instance
        user = manager.user

        send_email.delay(
            template_path="emails/notify_promotion.html",
            to_email=user.email,
            subject="You've been promoted to Manager!",
            context={
                'verification_code': manager.promotion_date,
                'first_name': user.first_name,
                'manager_token': manager.token
            }
        )
