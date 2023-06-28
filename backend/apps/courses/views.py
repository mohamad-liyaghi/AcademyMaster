from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from courses.permissions import (
    CanAddCourse,
)
from courses.serializers import (
    CourseCreateSerializer,
)
from managers.permissions import IsManager


@extend_schema_view(
    post=extend_schema(
        description='''Create a new course and assign to a teacher.''',
        request=CourseCreateSerializer,
        responses={
            '201': 'ok',
            '400': 'Invalid data',
            '403': 'Permission denied',
        },
        tags=['Courses'],
    ),
)
class TeacherCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsManager, CanAddCourse]
    serializer_class = CourseCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}
