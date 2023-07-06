from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from .permissions import (
    CanRetrieveEnrollment,
)
from .serializers import (
    EnrollmentCreateSerializer,
    EnrollmentRetrieveSerializer,
    EnrollmentUpdateSerializer,
    EnrollmentListSerializer,
)
from .models import Enrollment
from core.permissions import IsStudent, IsManager


@extend_schema_view(
    post=extend_schema(
        description='''Create a pending enrollment for user.''',
        request=EnrollmentCreateSerializer,
        responses={
            '201': 'ok',
            '400': 'Bad request',
            '401': 'Unauthorized',
            '403': 'Permission denied',
        },
        tags=['Enrollments'],
    ),
)
class EnrollmentCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = EnrollmentCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@extend_schema_view(
    get=extend_schema(
        description='''Retrieve an enrollment by token.''',
        responses={
            '200': 'ok',
            '401': 'Unauthorized',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Enrollments'],
    ),
)
class EnrollmentRetrieveView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, CanRetrieveEnrollment)
    serializer_class = EnrollmentRetrieveSerializer

    def get_object(self):
        enrollment = get_object_or_404(
            Enrollment.objects.select_related('course', 'user'),
            token=self.kwargs['enrollment_token']
        )
        self.check_object_permissions(self.request, enrollment)
        return enrollment


@extend_schema_view(
    patch=extend_schema(
        description='''Update an enrollment by token.''',
        request=EnrollmentUpdateSerializer,
        responses={
            '200': 'ok',
            '400': 'Bad request',
            '401': 'Unauthorized',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Enrollments'],
    ),
    put=extend_schema(
        description='''Update an enrollment by token.''',
        request=EnrollmentUpdateSerializer,
        responses={
            '200': 'ok',
            '400': 'Bad request',
            '401': 'Unauthorized',
            '403': 'Permission denied',
            '404': 'Not found',
        },
        tags=['Enrollments'],
    ),
)
class EnrollmentUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, CanRetrieveEnrollment)
    serializer_class = EnrollmentUpdateSerializer

    def get_object(self):
        enrollment = get_object_or_404(
            Enrollment,
            token=self.kwargs['enrollment_token']
        )
        self.check_object_permissions(self.request, enrollment)
        return enrollment


@extend_schema_view(
    get=extend_schema(
        description='''List all enrollments.''',
        responses={
            '200': 'ok',
            '401': 'Unauthorized',
            '403': 'Permission denied',
        },
        tags=['Enrollments'],
    ),
)
class EnrollmentListView(ListAPIView):
    permission_classes = (IsAuthenticated, IsManager | IsStudent)
    serializer_class = EnrollmentListSerializer

    def get_queryset(self):
        '''
        Return all enrollments if user is manager, otherwise return
        user enrollments.
        '''
        enrollments = Enrollment.objects.select_related(
            'course', 'user', 'user__profile'
        ).order_by('-created_at')

        if self.request.user.is_student():
            return enrollments.filter(user=self.request.user)

        return enrollments
