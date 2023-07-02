from celery import shared_task
from enrollments.models import Enrollment, EnrollmentStatus
from datetime import datetime, timedelta


@shared_task
def auto_delete_pending_enrollment():
    '''Delete pending enrollments after a day without payment'''
    yesterday = datetime.now() - timedelta(days=1)
    enrollments = Enrollment.objects.filter(
        status=EnrollmentStatus.PENDING,
        created_at__lte=yesterday
    )
    enrollments.delete()
    return f'{enrollments.count()} pending enrollments deleted'
