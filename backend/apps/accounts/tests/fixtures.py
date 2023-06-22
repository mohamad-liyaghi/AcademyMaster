import pytest
from faker import Faker
from accounts.models import Account

faker = Faker()


@pytest.fixture
def deactive_account():
    return Account.objects.create_user(
        email=faker.email(),
        password=faker.password()
    )


@pytest.fixture
def active_account():
    account = Account.objects.create_user(
        email=faker.email(),
        password=faker.password()
    )
    account.is_active = True
    account.save()
    return account


@pytest.fixture
def superuser():
    return Account.objects.create_superuser(
        email=faker.email(),
        password=faker.password()
    )
