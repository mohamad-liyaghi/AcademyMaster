import pytest


@pytest.mark.django_db
def test_inactive_account_is_not_active(inactive_account):
    assert not inactive_account.is_active


@pytest.mark.django_db
def test_active_account_is_active(active_account):
    assert active_account.is_active


@pytest.mark.django_db
def test_superuser_is_superuser(superuser):
    assert superuser.is_superuser
