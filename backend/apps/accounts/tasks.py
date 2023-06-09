from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from accounts.models import Account, VerificationCode


@shared_task
def delete_expired_codes():
    '''Delete expired verification codes.'''
    current_time = timezone.now()
    expired_codes = VerificationCode.objects.filter(
        Q(expire_at__lte=current_time) | Q(retry_count__gte=5)
    )
    count = expired_codes.count()
    expired_codes.delete()
    return f"{count} expired verification codes deleted."


@shared_task
def delete_deactivated_users():
    '''
    Delete deactivated users who haven't
    verified their accounts within the last 24 hours.
    '''
    day_before = timezone.now() - timedelta(hours=24)
    deactivated_users = Account.objects.filter(
        is_active=False,
        date_joined__lte=day_before
    )
    count = deactivated_users.count()
    deactivated_users.delete()
    return f"{count} deactivated users deleted."
