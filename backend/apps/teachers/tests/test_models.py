import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import PermissionDenied
from teachers.models import Teacher


@pytest.mark.django_db
class TestTeacherModel:
    def test_is_teacher(self, teacher_account):
        assert teacher_account.is_teacher()

    def test_teacher_user_has_token(self, teacher_account):
        assert teacher_account.token is not None

    def test_duplication_promotion(self, teacher_account):
        with pytest.raises(IntegrityError):
            Teacher.objects.create(user=teacher_account)

    def test_promote_by_accessed_manager(
        self, active_account, accessed_manager_account
    ):
        teacher = Teacher.objects.create(
            user=active_account, promoted_by=accessed_manager_account
        )
        assert accessed_manager_account.has_perm(
            perm_object=Teacher.get_permission("add")
        )
        teacher.delete()

    def test_promote_by_superuser(self, active_account, superuser):
        teacher = Teacher.objects.create(user=active_account, promoted_by=superuser)
        assert teacher.promoted_by == superuser

    def test_promote_by_manager_no_perm(self, manager_account, active_account):
        assert not manager_account.has_perm(perm_object=Teacher.get_permission("add"))
        with pytest.raises(PermissionDenied):
            Teacher.objects.create(user=active_account, promoted_by=manager_account)
