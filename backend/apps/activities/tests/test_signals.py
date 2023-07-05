import pytest
from activities.models import Activity


@pytest.mark.django_db
def test_create_activity(create_success_enrollment):
    assert Activity.objects.count() == 1
