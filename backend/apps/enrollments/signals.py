from django.dispatch import receiver
from django.db.models.signals import post_save

from enrollments.models import Enrollment
from apps.core.tasks import send_email


@receiver(post_save, sender=Enrollment)
def send_enrollment_email(sender, instance, created, **kwargs):
    """Send an email to the user when they are enrolled in a course"""
    if created:
        enrollment = instance
        account = enrollment.user
        course = enrollment.course

        send_email.delay(
            template_path="emails/enrollment.html",
            to_email=account.email,
            subject="Checkout your new enrollment!",
            context={
                "first_name": account.first_name,
                "course_title": course.title,
                "course_token": course.token,
                "enrollment_token": enrollment.token,
                "enrollment_date": enrollment.created_at,
            },
        )
