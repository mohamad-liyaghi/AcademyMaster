from django.db import models


class WeekDays(models.TextChoices):
    """A choice field for days of the week"""

    SATURDAY = (0, "Saturday")
    SUNDAY = (1, "Sunday")
    MONDAY = (2, "Monday")
    TUESDAY = (3, "Tuesday")
    WEDNESDAY = (4, "Wednesday")
    THURSDAY = (5, "Thursday")
    FRIDAY = (6, "Friday")
