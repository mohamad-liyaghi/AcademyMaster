import pytest
from django.contrib.auth.models import Permission
from managers.models import Manager


@pytest.fixture
def manager_account(active_account):
    Manager.objects.create_with_permissions(
        user=active_account,
        permissions=[]
    )
    return active_account


@pytest.fixture
def accessed_manager_account(active_account):
    Manager.objects.create_with_permissions(
        user=active_account,
        permissions=[
            *Permission.objects.all()
        ]
    )
    return active_account
