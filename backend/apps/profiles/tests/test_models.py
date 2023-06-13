import pytest
from datetime import date
from django.core.exceptions import ValidationError
from profiles.models import Profile
from core.tests import user, superuser


@pytest.mark.django_db
class TestProfileModel:

    def test_create_profile(self, superuser):
        assert Profile.objects.count() == 1

    def test_deactive_user_profile(self, user):
        assert Profile.objects.count() == 0

    def test_create_profile_active_user(self, user):
        user.is_active = True
        user.save()
        assert Profile.objects.count() == 1

    def test_create_profile_update_twice(self, user):
        user.is_active = True
        user.save()
        assert Profile.objects.count() == 1
        user.first_name = 'Updated'
        user.save()
        assert Profile.objects.count() == 1

    def test_phone_number_format(self, superuser):
        correct_number = '+989909901234'
        superuser.profile.phone_number = correct_number
        superuser.profile.birth_date = date(1989, 1, 1)
        superuser.profile.address = 'fake addr'
        superuser.profile.passport_id = '1234'
        superuser.profile.save()
        assert superuser.profile.phone_number == correct_number

    def test_age_property(self, superuser):
        today = date.today()
        birth_date = superuser.profile.birth_date = date(1989, 1, 1)
        superuser.profile.birth_date = date(1989, 1, 1)
        superuser.profile.phone_number = '+989909901234'
        superuser.profile.address = 'fake addr'
        superuser.profile.passport_id = '1234'
        superuser.profile.save()

        age_years = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age_years -= 1

        assert superuser.profile.age == age_years

    def test_update_profile_null_value(self, superuser):
        with pytest.raises(ValidationError):
            superuser.profile.address = 'Fake addr'
            superuser.profile.save()

    def test_update_profile_correct_value(self, superuser):
        birth_date = date(1989, 1, 1)
        phone_number = '+989909901234'
        address = 'fake addr'
        passport_id = '1234'
        superuser.profile.birth_date = birth_date
        superuser.profile.phone_number = phone_number
        superuser.profile.address = address
        superuser.profile.passport_id = passport_id
        superuser.profile.save()

        assert superuser.profile.birth_date == birth_date
        assert superuser.profile.phone_number == phone_number
        assert superuser.profile.address == address
        assert superuser.profile.passport_id == passport_id
