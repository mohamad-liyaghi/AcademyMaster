from django.db import models
from django.core.validators import RegexValidator
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

    birth_date = models.DateField()
    address = models.CharField(max_length=150)
    passport_id = models.CharField(max_length=15)

    PHONE_NUMBER_REGEX = r'^\+98\d{10}$'
    phone_number = models.CharField(
        validators=[RegexValidator(PHONE_NUMBER_REGEX)],
        max_length=13,
        unique=True,
    )

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def age(self):
        today = date.today()
        age_years = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age_years -= 1

        return age_years
