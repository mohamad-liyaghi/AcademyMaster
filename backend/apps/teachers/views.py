from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from teachers.permissions import (
    CanAddTeacher,
)
from teachers.serializers import TeacherCreateSerializer


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
class ManagerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanAddTeacher]
    serializer_class = TeacherCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}
