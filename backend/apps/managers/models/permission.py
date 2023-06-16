from django.db import models


class ManagerPermission(models.TextChoices):
    PROMOTE = ('promote_manager', 'Can promote a user to manager')
    DEMOTE = ('demote_manager', 'Can demote a manager to user')
