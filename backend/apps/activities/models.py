from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied
from core.models import AbstractToken
from courses.models import Course, CourseStatus
from enrollments.models import Enrollment, EnrollmentStatus


class Activity(AbstractToken):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="activities"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activities"
    )

    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="activities"
    )

    attendance = models.JSONField(blank=True, null=True)
    final_mark = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["course", "user"]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Activity {self.user}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.course = self.enrollment.course
            self.user = self.enrollment.user
            self.final_mark = None
            self.__validate_enrollment()

        if self.final_mark:
            self.__validate_final_mark()

        return super().save(*args, **kwargs)

    def __validate_enrollment(self):
        """Make sure the enrollment is successfull."""
        if self.enrollment.status != EnrollmentStatus.SUCCESS:
            raise PermissionDenied(
                "You can only create an activity for a successfull enrollment."
            )

    def __validate_final_mark(self):
        """
        Only activities with course status of COMPLETED can have final_mark.
        """
        if self.course.status != CourseStatus.COMPLETED:
            raise PermissionDenied(
                "You can only add a final mark for a finished course."
            )
