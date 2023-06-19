from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts.managers import AccountManager
from core.models import AbstractToken


class Account(AbstractBaseUser, PermissionsMixin, AbstractToken):
    # TODO: Role is temporarly, remove after implementing Managers/Teachers
    class Role(models.TextChoices):
        ADMIN = 'a', 'Admin'
        MANAGER = 'm', 'Manager'
        TEACHER = 't', 'Teacher'
        STUDENT = 's', 'Student'

    username = None
    email = models.EmailField(unique=True, max_length=255)

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.STUDENT
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AccountManager()

    class Meta:
        db_table = 'users'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self) -> bool:
        return bool(self.is_superuser)

    def is_admin(self) -> bool:
        return bool(self.is_staff)

    def is_manager(self) -> bool:
        try:
            return bool(self.manager)
        except Exception:
            return False

    def is_teacher(self) -> bool:
        try:
            return bool(self.teacher)
        except Exception:
            return False

    def is_student(self) -> bool:
        return bool(self.role == 's')

    def __str__(self) -> str:
        return str(self.email)
