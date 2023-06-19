from django.dispatch import receiver
from django.db.models.signals import post_save

from managers.models import Manager
from apps.core.tasks import send_email


@receiver(post_save, sender=Manager)
def send_manager_promotion_email(sender, created, instance, **kwargs):
    if created:
        manager = instance
        user = manager.user
        promoter_full_name = (
            instance.promoted_by.full_name
            if instance.promoted_by else None
        )

        send_email.delay(
            template_path="emails/notify_manager_promotion.html",
            to_email=user.email,
            subject="You've been promoted to Manager!",
            context={
                'promotion_date': manager.promotion_date,
                'promoter': promoter_full_name,
                'first_name': user.first_name,
                'manager_token': manager.token
            }
        )
