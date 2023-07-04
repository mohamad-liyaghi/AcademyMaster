import pytest


@pytest.mark.django_db
def test_get_activity(get_activity):
    assert get_activity is not None
