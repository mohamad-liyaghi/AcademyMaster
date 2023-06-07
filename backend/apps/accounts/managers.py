from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):

    def create_user(self, email: str, password: str, **kwargs):

        email = self.normalize_email(email)

        is_active = False
        user = self.model(
            email=email,
            is_active=is_active,
            role="s",
            **kwargs
        )

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email: str, password: str, **kwargs):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_active=True,
            is_superuser=True,
            role="a",
            **kwargs
        )

        user.set_password(password)

        user.save()

        return user
