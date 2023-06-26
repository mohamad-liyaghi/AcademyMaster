import pytest


@pytest.mark.django_db
def test_deactive_account(deactive_account):
    assert not deactive_account.is_active


@pytest.mark.django_db
def test_active_account(active_account):
    assert active_account.is_active


@pytest.mark.django_db
def test_superuser(superuser):
    assert superuser.is_superuser
