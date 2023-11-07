import pytest
from django.contrib.auth.models import Permission
from managers.models import Manager
from core.tests.utils import create_account


@pytest.fixture(scope="class")
def manager_account(django_db_blocker, django_db_setup):
    with django_db_blocker.unblock():
        active_account = create_account(is_active=True)
        Manager.objects.create_with_permissions(user=active_account, permissions=[])
        yield active_account


@pytest.fixture(scope="class")
def accessed_manager_account(django_db_blocker, django_db_setup):
    with django_db_blocker.unblock():
        active_account = create_account(is_active=True)
        Manager.objects.create_with_permissions(
            user=active_account, permissions=[*Permission.objects.all()]
        )
        yield active_account
