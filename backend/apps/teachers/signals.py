from django.dispatch import receiver
from django.db.models.signals import post_save

from teachers.models import Teacher
from apps.core.tasks import send_email


@receiver(post_save, sender=Teacher)
def send_teacher_promotion_email(sender, created, instance, **kwargs):
    '''Send an email to user when promoted as teacher'''
    if created:
        instance = instance
        user = instance.user
        promoter_full_name = (
            instance.promoted_by.full_name
            if instance.promoted_by else None
        )

        send_email.delay(
            template_path="emails/notify_teacher_promotion.html",
            to_email=user.email,
            subject="You've been promoted to Teacher!",
            context={
                'promoter': promoter_full_name,
                'promotion_date': instance.promotion_date,
                'first_name': user.first_name,
                'teacher_token': instance.token
            }
        )
