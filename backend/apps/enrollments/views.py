from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from .permissions import (
    AllowStudentOnly,
    IsManagerOrObjectOwner,
)
from .serializers import (
    EnrollmentCreateSerializer,
    EnrollmentRetrieveSerializer,
)
from .models import Enrollment


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
    permission_classes = (IsAuthenticated, AllowStudentOnly)
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
    permission_classes = (IsAuthenticated, IsManagerOrObjectOwner)
    serializer_class = EnrollmentRetrieveSerializer

    def get_object(self):
        enrollment = get_object_or_404(
            Enrollment.objects.select_related('course', 'user'),
            token=self.kwargs['enrollment_token']
        )
        self.check_object_permissions(self.request, enrollment)
        return enrollment