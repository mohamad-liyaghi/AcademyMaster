from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from courses.permissions import (
    CanAddCourse,
    CanUpdateCourse,
    CanDeleteCourse,
)
from courses.serializers import (
    CourseCreateSerializer,
    CourseRetrieveSerializer,
    CourseUpdateSerializer
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


@extend_schema_view(
    put=extend_schema(
        description='''Update an enrolling course.''',
        request=CourseUpdateSerializer,
        responses={
            '201': 'ok',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Courses'],
    ),
    patch=extend_schema(
        description='''Update an enrolling course.''',
        request=CourseUpdateSerializer,
        responses={
            '201': 'ok',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Courses'],
    ),
)
class CourseUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsManager, CanUpdateCourse]
    serializer_class = CourseUpdateSerializer

    def get_object(self):
        course = get_object_or_404(
            Course,
            token=self.kwargs['course_token']
        )
        self.check_object_permissions(self.request, course)
        return course


# TODO update status
@extend_schema_view(
    delete=extend_schema(
        description='''Delete a course.''',
        responses={
            '201': 'ok',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Courses'],
    ),
)
class CourseDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsManager, CanDeleteCourse]

    def get_object(self):
        course = get_object_or_404(
            Course,
            token=self.kwargs['course_token']
        )
        self.check_object_permissions(self.request, course)
        return course
