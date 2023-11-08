from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied
from core.models import AbstractToken
from managers.managers import ManagerManager
from core.models import AbstractPermission


class Manager(AbstractToken, AbstractPermission):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    promoted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="promoted_managers",
    )

    promotion_date = models.DateTimeField(auto_now_add=True)

    objects = ManagerManager()

    class Meta:
        db_table = "managers"
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    def __str__(self) -> str:
        return f"{self.user} (Manager)"

    def save(self, *args, **kwargs):
        if not self.pk and self.promoted_by:
            if not self.user.is_student():
                raise PermissionDenied("Promoted user must be student.")

            # Check permissions
            self._validate_creator(creator=self.promoted_by)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove all manager permissions of a user while deleting
        self.user.user_permissions.clear()
        return super().delete(*args, **kwargs)
