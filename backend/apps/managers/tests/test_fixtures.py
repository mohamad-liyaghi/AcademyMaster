import pytest
from managers.models import Manager


@pytest.mark.django_db
def test_manager_is_manager(manager_account):
    assert manager_account.is_manager()


@pytest.mark.django_db
def test_accessed_manager_is_manager(accessed_manager_account):
    assert accessed_manager_account.is_manager()


@pytest.mark.django_db
def test_manager_permission(manager_account):
    assert not manager_account.has_perm(
        perm_object=Manager.get_permission('add')
    )


@pytest.mark.django_db
def test_accessed_manager_permission(accessed_manager_account):
    assert accessed_manager_account.has_perm(
        perm_object=Manager.get_permission('add')
    )


@pytest.mark.django_db
def test_manager_no_permission(manager_account):
    assert not manager_account.has_perm(
        perm_object=Manager.get_permission('add')
    )
