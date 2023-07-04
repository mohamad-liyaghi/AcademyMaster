from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied
from core.models import AbstractPermission, AbstractToken


class Teacher(AbstractToken, AbstractPermission):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    promoted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='promoted_teachers'
    )

    description = models.TextField(
        max_length=250,
        default='This teacher has not yet provided a description'
    )

    promotion_date = models.DateTimeField(auto_now_add=True)
    contact_links = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self) -> str:
        return f'{self.user} (Teacher)'

    def save(self, *args, **kwargs):
        if not self.pk and self.promoted_by:
            if not self.user.is_student():
                raise PermissionDenied("Promoted user must be student.")
            # Check for permissions
            self._validate_creator(creator=self.promoted_by)
        return super().save(*args, **kwargs)
