from django.dispatch import receiver
from django.db.models.signals import post_save

from enrollments.models import Enrollment, EnrollmentStatus
from .models import Activity


@receiver(post_save, sender=Enrollment)
def create_activity_after_successfull_enrollment(sender, instance, **kwargs):
    '''Create an activity after a successfull enrollment.'''
    if instance.status == EnrollmentStatus.SUCCESS:
        Activity.objects.create(user=instance.user, enrollment=instance)
