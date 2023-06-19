from django.urls import reverse
from rest_framework import status
import pytest
from core.tests import user, teacher, superuser, api_client, manager
from django.contrib.auth import get_user_model
from teachers.models import Teacher
from accounts.models import Account


@pytest.mark.django_db
class TestTeacherCreateView:

    def setup(self):
        self.create_url = reverse('teachers:create_teacher')
        self.user = Account.objects.create_user(
            email='teacher@email.com', password='1234EErr'
        )
        self.data = {
            "user": self.user.token,
        }

    def test_unauthorized(self, api_client):
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_teacher(self, api_client, superuser):
        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        print(resp)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.user.teacher.promoted_by == superuser

    def test_create_teacher_by_manager_permission_denied(self, api_client, manager):
        assert not manager.has_perm(
            Teacher.get_permission('add', return_str=True)
        )
        api_client.force_authenticate(manager)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_promote_non_student(self, api_client, manager, superuser):
        assert not manager.is_student()
        self.data['user'] = manager.token

        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplication_promote(self, api_client, superuser, teacher):
        assert not teacher.is_student()
        self.data['user'] = teacher.token
        api_client.force_authenticate(superuser)
        resp = api_client.post(self.create_url, self.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
