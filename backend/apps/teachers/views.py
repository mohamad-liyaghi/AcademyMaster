from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from teachers.permissions import (
    CanAddTeacher,
)
from teachers.serializers import (
    TeacherCreateSerializer,
    TeacherRetrieveSerializer
)
from teachers.models import Teacher


@extend_schema_view(
    post=extend_schema(
        description='''Add a new teacher.''',
        request=TeacherCreateSerializer,
        responses={
            '201': 'ok',
            '400': 'Invalid data',
            '403': 'Permission denied',
        },
        tags=['Teachers'],
    ),
)
class TeacherCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanAddTeacher]
    serializer_class = TeacherCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@extend_schema_view(
    get=extend_schema(
        description='''Detail page of a teacher.''',
        request=TeacherRetrieveSerializer,
        responses={
            '201': 'ok',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Teachers'],
    ),
)
class TeacherRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherRetrieveSerializer

    def get_object(self):
        return get_object_or_404(
            Teacher.objects.select_related('user'),
            token=self.kwargs['teacher_token']
        )
