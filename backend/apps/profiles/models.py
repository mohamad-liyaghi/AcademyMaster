from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from core.models import AbstractToken
from django.conf import settings
from datetime import date
from dateutil.relativedelta import relativedelta


class Profile(AbstractToken):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        default="assets/pictures/profiles/default-avatar.jpg",
    )

    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True, default=None)
    passport_id = models.CharField(max_length=15, null=True, default=None)

    PHONE_NUMBER_REGEX = r"^\+98\d{10}$"
    phone_number = models.CharField(
        validators=[RegexValidator(PHONE_NUMBER_REGEX)],
        max_length=13,
        null=True,
        default=None,
    )

    class Meta:
        db_table = "profiles"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def age(self):
        if not self.birth_date:
            return None

        age = relativedelta(date.today(), self.birth_date).years
        return age

    REQUIRED_FIELDS = ["birth_date", "address", "passport_id", "phone_number"]

    def __check_required_fields(self) -> None:
        """
        Ensure that required fields are not None.
        When an object is created by signal,
        some fields are None.
        User must update them and cannot insert None.
        """

        # Get attrs for REQUIRED FIELDS
        null_fields = [
            field for field in self.REQUIRED_FIELDS if getattr(self, field) is None
        ]

        # Raise error if there are null values
        if null_fields:
            raise ValidationError(f"Field (s) {null_fields} are required")

    def save(self, *args, **kwargs):
        if self.pk:
            self.__check_required_fields()

        return super().save(*args, **kwargs)
