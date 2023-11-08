from django.db import models


class CourseStatus(models.TextChoices):
    ENROLLING = ("EN", "Enrolling")
    IN_PROGRESS = ("IP", "In Progress")
    COMPLETED = ("CO", "Completed")
