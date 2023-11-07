from faker import Faker
from accounts.models import Account

faker = Faker()


def create_account(password: str = "1234PassWord", is_active: bool = False) -> Account:
    """Return an accounts instance."""
    return Account.objects.create_user(
        email=faker.email(), password=password, is_active=is_active
    )
