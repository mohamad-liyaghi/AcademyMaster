from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Permission
from accounts.managers import AccountManager
from core.models import AbstractToken
from .role import AccountRole


class Account(AbstractBaseUser, PermissionsMixin, AbstractToken, AccountRole):
    username = None
    email = models.EmailField(unique=True, max_length=255)

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = AccountManager()

    class Meta:
        db_table = "users"

    def has_perm(self, perm_object: Permission, perm_str: str = None, obj=None) -> bool:
        if not (perm_object or perm_str):
            raise ValueError("Either perm_object or perm_str is required")

        # Active admins have all permissions.
        if self.is_active and self.is_admin():
            return True

        # Check permission exists in user_permission
        elif self.user_permissions.filter(codename=perm_object.codename).exists():
            return True

        return super().has_perm(perm_str, obj)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self) -> bool:
        return bool(self.is_superuser)

    def __str__(self) -> str:
        return f"{self.email} ({self.first_name})"
