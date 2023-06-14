from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from managers.managers import ManagerManager


class ManagerPermission(models.TextChoices):
    PROMOTE = ('promote_manager', 'Can promote a user to manager')
    DEMOTE = ('demote_manager', 'Can demote a manager to user')


class Manager(models.Model):
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
        permissions = [
            (permission.value, permission.label)
            for permission in ManagerPermission
        ]
        db_table = 'managers'
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

    def __str__(self) -> str:
        return f'{self.user} (Manager)'

    def can_promote(self) -> bool:
        """Check if the user has permission to promote a manager."""
        return self.user.user_permissions.filter(
            codename=ManagerPermission.PROMOTE.value
        ).exists()

    def can_demote(self) -> bool:
        """Check if the user has permission to demote a manager."""
        return self.user.user_permissions.filter(
            codename=ManagerPermission.DEMOTE.value
        ).exists()

    def validate_promoter(self) -> None:
        """Check if the promoted user has the required permissions."""

        # admins can promote managers
        if self.promoted_by.is_admin():
            return

        if not self.promoted_by.is_manager():
            raise ValidationError("Promoter must be a manager.")

        if not self.promoted_by.manager.can_promote():
            raise ValidationError("Permission denied.")

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.promoted_by:
                self.validate_promoter()

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove all manager permissions of a user while deleting
        self.__class__.objects.remove_permissions(
            user=self.user,
            codenames=[*ManagerPermission]
        )
        return super().delete(*args, **kwargs)
