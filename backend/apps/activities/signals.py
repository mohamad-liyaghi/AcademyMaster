from django.dispatch import receiver
from django.db.models.signals import post_save

from enrollments.models import Enrollment, EnrollmentStatus
from .models import Activity
from core.tasks import send_email


@receiver(post_save, sender=Enrollment)
def create_activity_after_successfull_enrollment(sender, instance, **kwargs):
    '''Create an activity after a successfull enrollment.'''
    if instance.status == EnrollmentStatus.SUCCESS:
        Activity.objects.create(user=instance.user, enrollment=instance)


@receiver(post_save, sender=Activity)
def send_email_after_activity_creation(sender, instance, created, **kwargs):
    '''Send an email after an activity is created.'''
    if created:
        user = instance.user
        course = instance.course

        send_email.delay(
            template_path="emails/activity_creation.html",
            to_email=user.email,
            subject='Checkout your new activity!',
            context={
                'first_name': user.first_name,
                'course_title': course.title,
                'course_token': course.token,
                'activity_token': instance.token,
            }
        )
