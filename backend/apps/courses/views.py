from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from courses.permissions import (
    CanAddCourse,
)
from courses.serializers import (
    CourseCreateSerializer,
    CourseRetrieveSerializer,
)
from courses.models import Course
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
class CourseCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsManager, CanAddCourse]
    serializer_class = CourseCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@extend_schema_view(
    get=extend_schema(
        description='''Retrieve a course.''',
        request=CourseRetrieveSerializer,
        responses={
            '201': 'ok',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Courses'],
    ),
)
class CourseRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseRetrieveSerializer

    def get_object(self):
        return get_object_or_404(
            Course.objects.select_related(
                'instructor', 'instructor__user', 'assigned_by', 'prerequisite'
            ),
            token=self.kwargs['course_token']
        )
