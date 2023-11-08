from django.db import models
import uuid


class AbstractToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True
