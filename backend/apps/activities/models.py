from django.db import models
from django.conf import settings
from core.models import AbstractToken
from courses.models import Course
from enrollments.models import Enrollment


class Activity(AbstractToken):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    attendance = models.JSONField(blank=True, null=True)
    final_mark = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'user']
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.course = self.enrollment.course

        return super().save(*args, **kwargs)
