from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from activities.permissions import (
    CanRetrieveActivity,
    CanUpdateActivity,
    IsCourseInstructor,
)
from activities.serializers import (
    ActivityRetrieveSerializer,
    ActivityUpdateSerializer,
    ActivityListSerializer,
)
from activities.models import Activity
from courses.models import Course


@extend_schema_view(
    get=extend_schema(
        description='''Register a new user.''',
        responses={
            '200': ActivityRetrieveSerializer,
            '403': 'Forbidden',
            '400': 'Unauthorized',
            '404': 'Not found',
        },
        tags=['Activities'],
    ),
)
class ActivityRetrieveView(RetrieveAPIView):
    '''Retrieve an activity'''
    queryset = Activity.objects.all()
    serializer_class = ActivityRetrieveSerializer
    permission_classes = [IsAuthenticated, CanRetrieveActivity]

    def get_object(self):
        activity = get_object_or_404(
            Activity.objects.select_related(
                'user', 'course', 'enrollment', 'user__profile'
            ),
            token=self.kwargs['activity_token'],
            course__token=self.kwargs['course_token'],
        )
        self.check_object_permissions(self.request, activity)
        return activity


@extend_schema_view(
    patch=extend_schema(
        description='''Update an activity.''',
        request=ActivityUpdateSerializer,
        responses={
            '200': 'Updated',
            '403': 'Forbidden',
            '400': 'Unauthorized',
            '404': 'Not found',
        },
        tags=['Activities'],
    ),
    put=extend_schema(
        description='''Update an activity by its course instructor.''',
        request=ActivityUpdateSerializer,
        responses={
            '200': 'Updated',
            '403': 'Forbidden',
            '400': 'Unauthorized',
            '404': 'Not found',
        },
        tags=['Activities'],
    ),
)
class ActivityUpdateView(UpdateAPIView):
    serializer_class = ActivityUpdateSerializer
    permission_classes = [IsAuthenticated, CanUpdateActivity]

    def get_object(self):
        activity = get_object_or_404(
            Activity.objects.select_related('user', 'course', 'enrollment'),
            token=self.kwargs['activity_token'],
            course__token=self.kwargs['course_token'],
        )
        self.check_object_permissions(self.request, activity)
        return activity


@extend_schema_view(
    get=extend_schema(
        description='''List all activities of a course.''',
        responses={
            '200': 'ok',
            '403': 'Forbidden',
            '401': 'Unauthorized',
            '404': 'Not found',
        },
        tags=['Activities'],
    ),
)
class CourseActivityListView(ListAPIView):
    '''List all activities of a course'''
    serializer_class = ActivityListSerializer
    permission_classes = [IsAuthenticated, IsCourseInstructor]

    def get_queryset(self):
        course = get_object_or_404(
            Course.objects.select_related(
                'instructor',
            ),
            token=self.kwargs['course_token']
        )

        # Check user permissions
        self.check_object_permissions(self.request, course)

        # Access the prefetched activities directly
        return course.activities.select_related(
            'user', 'user__profile'
        ).all()
