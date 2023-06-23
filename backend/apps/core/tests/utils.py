from faker import Faker
from accounts.models import Account

faker = Faker()


def create_account(is_active=False):
    return Account.objects.create_user(
        email=faker.email(),
        password=faker.password(),
        is_active=is_active
    )
