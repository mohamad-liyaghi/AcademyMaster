import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from teachers.models import Teacher
from core.tests import user, superuser, manager, teacher


@pytest.mark.django_db
class TestTeacherModel:
    def test_is_teacher(self, user):
        Teacher.objects.create(user=user)
        assert user.is_teacher()

    def test_teacher_has_token(self, teacher):
        assert teacher.token is not None

    def test_duplication_promotion(self, teacher):
        with pytest.raises(IntegrityError):
            Teacher.objects.create(user=teacher)

    def test_promote_by_manager(self, user, manager):
        assert not manager.has_perm(perm_object=Teacher.get_permission('add'))

        manager.user_permissions.add(
             Teacher.get_permission('add')
        )
        assert manager.has_perm(perm_object=Teacher.get_permission('add'))
        Teacher.objects.create(user=user, promoted_by=manager)

    def test_promote_by_superuser(self, user, superuser):
        teacher = Teacher.objects.create(user=user, promoted_by=superuser)
        assert teacher.promoted_by == superuser

    def test_promote_by_manager_no_permission(self, manager, user):
        assert not manager.has_perm(perm_object=Teacher.get_permission('add'))

        with pytest.raises(ValidationError):
            Teacher.objects.create(user=user, promoted_by=manager)
