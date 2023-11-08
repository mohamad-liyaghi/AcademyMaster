from django.db import models


class EnrollmentStatus(models.TextChoices):
    PENDING = ("p", "Pending")
    SUCCESS = ("s", "Success")
    FAILED = ("f", "Failed")
