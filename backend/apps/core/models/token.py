from django.db import models
from core.utils import generate_unique_token


class AbstractToken(models.Model):
    token = models.CharField(max_length=32, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_unique_token()

        super().save(*args, **kwargs)
