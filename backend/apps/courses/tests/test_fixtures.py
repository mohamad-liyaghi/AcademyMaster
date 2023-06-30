import pytest
from courses.models import Course


@pytest.mark.django_db
def test_create_course(create_course):
    assert Course.objects.count() == 1
