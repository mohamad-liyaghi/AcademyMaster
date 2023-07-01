from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from .permissions import (
    AllowStudentOnly,
)
from .serializers import (
    EnrollmentCreateSerializer,
)


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
        tags=['Courses'],
    ),
)
class EnrollmentCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, AllowStudentOnly)
    serializer_class = EnrollmentCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}
