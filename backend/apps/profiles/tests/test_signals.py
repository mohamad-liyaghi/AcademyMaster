import pytest
from profiles.models import Profile


@pytest.mark.django_db
class TestProfileSignal:
    """
    There is a signal which creates a profile for user when user gets activated
    """

    def test_create_profile(self, superuser):
        assert Profile.objects.filter(user=superuser).exists()

    def test_deactive_user_profile(self, inactive_account):
        """Signal doesnt create profile for inactive accounts"""
        assert not Profile.objects.filter(user=inactive_account).exists()

    def test_create_profile_active_user(self, active_account):
        assert Profile.objects.filter(user=active_account).exists()

    def test_dont_create_profile_update_twice(self, active_account):
        """Signal does not create profile for a user twice (when updating)"""
        assert Profile.objects.filter(user=active_account).count() == 1
        active_account.first_name = "Updated"
        active_account.save()
        assert Profile.objects.filter(user=active_account).count() == 1
