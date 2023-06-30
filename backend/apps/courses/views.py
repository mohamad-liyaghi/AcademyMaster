from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from elasticsearch_dsl import Q
from rest_framework.response import Response
from rest_framework import status
from courses.permissions import (
    CanAddCourse,
    CanUpdateCourse,
    CanDeleteCourse,
)
from courses.serializers import (
    CourseCreateSerializer,
    CourseRetrieveSerializer,
    CourseUpdateSerializer,
    CourseListSerializer,
)
from courses.models import Course, CourseStatus
from courses.documents import CourseDocument
from managers.permissions import IsManager


@extend_schema_view(
    post=extend_schema(
        description='''Create a new course and assign to a teacher.''',
        request=CourseCreateSerializer,
        responses={
            '201': 'ok',
            '400': 'Invalid data',
            '401': 'Unauthorized',
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
            '200': 'ok',
            '401': 'Unauthorized',
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
            '200': 'ok',
            '400': 'Course is not enrolling',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Courses'],
    ),
    patch=extend_schema(
        description='''Update an enrolling course.''',
        request=CourseUpdateSerializer,
        responses={
            '200': 'ok',
            '400': 'Cannot delete in-progress/completed courses.',
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


@extend_schema_view(
    delete=extend_schema(
        description='''Delete a course.''',
        responses={
            '204': 'ok',
            '400': 'Cannot delete in-progress/completed courses.',
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

    def destroy(self, request, *args, **kwargs):
        if self.get_object().status != CourseStatus.ENROLLING:
            return Response(
                {'detail': 'Cannot delete in-progress/completed courses.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        description='''List of all courses.''',
        request=CourseListSerializer,
        responses={
            '200': 'ok',
            '401': 'Unauthorized'
        },
        tags=['Courses'],
    ),
)
class CourseListView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CourseListSerializer

    def get_queryset(self):
        # Filter it there is a search query
        if (search_query := self.request.query_params.get('search')):
            return CourseDocument.search().query(
                Q(
                    'multi_match', query=search_query,
                    fields=[
                            'title',
                            'description',
                        ]
                )
            ).to_queryset()

        return Course.objects.select_related(
            'instructor', 'instructor__user'
        ).order_by('-start_date')

# TODO get only enrolling courses
