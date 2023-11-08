import pytest
from activities.models import Activity


@pytest.mark.django_db
def test_create_activity(create_success_enrollment):
    assert Activity.objects.filter(
        user=create_success_enrollment.user,
        enrollment=create_success_enrollment,
    ).exists()
