from django.db import models


class CourseLevel(models.TextChoices):
    A1 = ("A1", "Beginner")
    A2 = ("A2", "Elementary")
    B1 = ("B1", "Pre-Intermediate")
    B2 = ("B2", "Intermediate")
    C1 = ("C1", "Upper-Intermediate")
    C2 = ("C2", "Advance")
