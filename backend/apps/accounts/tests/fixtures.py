import pytest
from faker import Faker
from accounts.models import Account
from core.tests.utils import create_account

faker = Faker()

BASE_PASSWORD = "1234UserPASS"


@pytest.fixture(scope="class")
def inactive_account(django_db_setup, django_db_blocker) -> Account:
    """Return an inactive accounts instance."""
    with django_db_blocker.unblock():
        yield create_account(password=BASE_PASSWORD)


@pytest.fixture(scope="class")
def active_account(django_db_setup, django_db_blocker) -> Account:
    """Return an active accounts instance."""
    with django_db_blocker.unblock():
        yield create_account(is_active=True, password=BASE_PASSWORD)


@pytest.fixture(scope="class")
def another_account(django_db_setup, django_db_blocker) -> Account:
    """Return an active accounts instance."""
    with django_db_blocker.unblock():
        yield create_account(is_active=True, password=BASE_PASSWORD)


@pytest.fixture(scope="class")
def superuser(django_db_setup, django_db_blocker) -> Account:
    with django_db_blocker.unblock():
        yield Account.objects.create_superuser(
            email=faker.email(), password=BASE_PASSWORD
        )
