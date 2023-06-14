from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from managers.models import Manager
from managers.permissions import CanPromotePermission, IsManagerPromoter
from managers.serializers import (
    ManagerCreateSerializer,
    ManagerUpdateSerializer
)


@extend_schema_view(
    post=extend_schema(
        description='''Add a new manager.''',
        request=ManagerCreateSerializer,
        responses={
            '201': 'ok',
            '400': 'Invalid data',
            '403': 'Permission denied',
        },
        tags=['Authentication'],
    ),
)
class ManagerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanPromotePermission]
    serializer_class = ManagerCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@extend_schema_view(
    post=extend_schema(
        description='''Update a managers permissions.''',
        request=ManagerCreateSerializer,
        responses={
            '200': 'ok',
            '400': 'Invalid data',
            '403': 'Permission denied',
        },
        tags=['Authentication'],
    ),
)
class ManagerUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsManagerPromoter]
    serializer_class = ManagerUpdateSerializer

    def get_object(self):
        manager = get_object_or_404(
            Manager,
            token=self.kwargs['manager_token']
        )
        self.check_object_permissions(self.request, manager)
        return manager
