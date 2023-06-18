from django.db import models
from django.conf import settings
from core.models import AbstractToken
from django.core.exceptions import ValidationError
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
        related_name='promoted_managers',
    )

    promotion_date = models.DateTimeField(auto_now_add=True)

    objects = ManagerManager()

    class Meta:
        db_table = 'managers'
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

    def __str__(self) -> str:
        return f'{self.user} (Manager)'

    def _validate_promoter(self) -> None:
        """Check if the promoted user has the required permissions."""

        # admins can promote managers
        if self.promoted_by.is_admin():
            return

        if not self.promoted_by.is_manager():
            raise ValidationError("Promoter must be a manager.")

        if not self.promoted_by.has_perm(
            self.__class__.get_permission('add')
        ):
            raise ValidationError("Permission denied.")

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.promoted_by:
                self._validate_promoter()

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove all manager permissions of a user while deleting
        self.user.user_permissions.clear()
        return super().delete(*args, **kwargs)
