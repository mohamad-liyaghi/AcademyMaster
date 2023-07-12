from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.models import AbstractToken
from courses.models import Course
from .enrollment_status import EnrollmentStatus


class Enrollment(AbstractToken):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='enrollments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    status = models.CharField(
        max_length=1,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Enrollment {self.user}"

    def _validate_enrollment(self) -> None:
        existing_enrollment = Enrollment.objects.filter(
            course=self.course,
            user=self.user,
        )
        if existing_enrollment:

            if existing_enrollment.filter(status=EnrollmentStatus.SUCCESS):
                raise ValidationError(
                    'You have already enrolled in this course'
                )
            elif existing_enrollment.filter(status=EnrollmentStatus.PENDING):
                raise ValidationError(
                    'You have already requested to enroll in this course'
                )

        return

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.course.price
            self._validate_enrollment()
        return super().save(*args, **kwargs)
