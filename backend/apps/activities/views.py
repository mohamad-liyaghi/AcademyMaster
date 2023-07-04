from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from activities.permissions import (
    CanRetrieveActivity,
)
from activities.serializers import (
    ActivityRetrieveSerializer,
)
from activities.models import Activity


@extend_schema_view(
    get=extend_schema(
        description='''Register a new user.''',
        responses={
            '200': ActivityRetrieveSerializer,
            '403': 'Forbidden',
            '400': 'Unauthorized',
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
            Activity.objects.select_related('user', 'course', 'enrollment'),
            token=self.kwargs['activity_token']
        )
        self.check_object_permissions(self.request, activity)
        return activity
