import pytest


@pytest.fixture(scope="class")
def get_activity(create_success_enrollment, django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        return create_success_enrollment.activities.first()
