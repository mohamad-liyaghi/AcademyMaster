import pytest


@pytest.mark.django_db
class TestAccountModel:

    def test_user_not_active(self, deactive_account):
        '''By default users are all deactive'''
        assert not deactive_account.is_active

    def test_superuser_is_active(self, superuser):
        '''By default superusers are active'''
        assert superuser.is_active

    def test_user_has_token(self, active_account, superuser):
        '''There is a AbstractToken model that creates token for each user'''
        assert active_account.token
        assert superuser.token

    def test_users_token_is_unique(self, active_account, superuser):
        '''All tokens for users are unique'''
        assert active_account.token != superuser.token
