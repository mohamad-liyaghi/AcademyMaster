import pytest


@pytest.fixture
def get_activity(create_success_enrollment):
    return create_success_enrollment.activities.first()
