import pytest
from rest_framework.test import APIClient
from accounts.models import Account
from managers.models import Manager


@pytest.fixture
def user():
    return Account.objects.create_user(
        email="simple@simple.com",
        password="1234USERnormal"
    )


@pytest.fixture
def superuser():
    return Account.objects.create_superuser(
        email="superuser@superuser.com",
        password="1234EErrSuperuser"
    )


@pytest.fixture
def manager():
    manager = Account.objects.create_user(
        email="manager@manager.com",
        password="1234USERnormal",
    )
    Manager.objects.create_with_permissions(user=manager, permissions=[])
    return manager


@pytest.fixture
def teacher():
    teacher = Account.objects.create_user(
        email="teacher@teacher.com",
        password="1234USERnormal",
    )
    teacher.role = Account.Role.TEACHER
    teacher.save()
    return teacher


@pytest.fixture
def api_client():
    return APIClient()
