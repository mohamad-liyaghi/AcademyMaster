import pytest


@pytest.mark.django_db
class TestAccountModel:
    def test_user_not_active(self, inactive_account):
        """By default users are all inactive"""
        assert not inactive_account.is_active

    def test_superuser_is_active(self, superuser):
        """By default superusers are active"""
        assert superuser.is_active

    def test_user_has_token_attr(self, active_account, superuser):
        """There is a AbstractToken model that creates token for each user"""
        assert active_account.token
        assert superuser.token

    def test_user_tokens_are_unique(self, active_account, superuser):
        """All tokens for users are unique"""
        assert active_account.token != superuser.token
