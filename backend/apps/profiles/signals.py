from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from profiles.models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_active_user(sender, instance, created, **kwargs):
    """Create profile for a user as soon as it is activated"""
    if instance.is_active:
        profile = Profile.objects.filter(user=instance)

        if not profile:
            Profile.objects.create(user=instance)
