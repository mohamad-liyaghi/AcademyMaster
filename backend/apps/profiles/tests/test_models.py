import pytest
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestProfileModel:
    @pytest.fixture(autouse=True)
    def setup(self, superuser):
        self.valid_data = {
            "phone_number": "+989909901234",
            "birth_date": date(1989, 1, 1),
            "address": "Unit 15, No.392, Q.Maqam Intersection, Beheshti st",
            "passport_id": "436712",
        }
        self.profile = superuser.profile
        self.update_profile(self.valid_data)

    def update_profile(self, data):
        self.profile.phone_number = data["phone_number"]
        self.profile.birth_date = data["birth_date"]
        self.profile.address = data["address"]
        self.profile.passport_id = data["passport_id"]
        self.profile.save()

    def test_phone_number_format(self):
        """Phone number format must be like +98 000 000 0000"""
        assert self.profile.phone_number == self.valid_data["phone_number"]

    def test_age_property(self):
        today = date.today()
        twenty_years_ago = today - relativedelta(years=20)
        self.update_profile({**self.valid_data, "birth_date": twenty_years_ago})
        assert self.profile.age == 20

    def test_update_profile_null_value(self):
        with pytest.raises(ValidationError):
            self.profile.phone_number = None
            self.profile.save()

    def test_update_profile_correct_value(self):
        self.update_profile(self.valid_data)
        assert self.profile.birth_date == self.valid_data["birth_date"]
        assert self.profile.phone_number == self.valid_data["phone_number"]
        assert self.profile.address == self.valid_data["address"]
        assert self.profile.passport_id == self.valid_data["passport_id"]
