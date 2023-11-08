import pytest
from courses.models import Course


@pytest.mark.django_db
def test_course_is_created(create_course):
    assert Course.objects.count() != 0
