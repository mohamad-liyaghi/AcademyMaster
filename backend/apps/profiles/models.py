from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from core.models import AbstractToken
from django.conf import settings
from datetime import date


class Profile(AbstractToken):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        default='assets/pictures/profiles/default-avatar.jpg',
    )

    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        default=None
    )
    passport_id = models.CharField(
        max_length=15,
        null=True,
        default=None
    )

    PHONE_NUMBER_REGEX = r'^\+98\d{10}$'
    phone_number = models.CharField(
        validators=[RegexValidator(PHONE_NUMBER_REGEX)],
        max_length=13,
        null=True,
        default=None
    )

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def age(self):
        birth_date = self.birth_date
        if not birth_date:
            return None

        today = date.today()
        age_years = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age_years -= 1

        return age_years

    def save(self, *args, **kwargs) -> None:
        '''
            Ensure that required fields are not None.
            When an object is created by signal, 
            some fields are None.
            User must update them and cannot insert None.
        '''

        if self.pk:
            # Get null fields
            null_fields = [
                field.name for field in self._meta.fields \
                if getattr(self, field.name) is None
            ]

            # Raise error if there are null values
            if null_fields:
                for null_field in null_fields:
                    raise ValidationError(f"{null_field} field is required")

        return super().save(*args, **kwargs)
