from django.db import models
from django.conf import settings


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

    class Meta:
        permissions = [
            (ManagerPermission.PROMOTE.value, ManagerPermission.PROMOTE.label),
            (ManagerPermission.DEMOTE.value, ManagerPermission.DEMOTE.label),
        ]
        db_table = 'managers'
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

    def __str__(self) -> str:
        return f'{self.user} (Manager)'
