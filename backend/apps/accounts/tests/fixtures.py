import pytest
from faker import Faker
from accounts.models import Account
from core.tests.utils import create_account

faker = Faker()


@pytest.fixture
def deactive_account():
    return create_account()


@pytest.fixture
def active_account():
    return create_account(is_active=True)


@pytest.fixture
def superuser():
    return Account.objects.create_superuser(
        email=faker.email(),
        password=faker.password()
    )
