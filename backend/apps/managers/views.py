from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from managers.models import Manager
from managers.permissions import (
    CanAddManager,
    CanDeleteManager,
    CanChangeManager,
)
from managers.serializers import (
    ManagerCreateSerializer,
    ManagerUpdateSerializer,
    ManagerRetrieveSerializer,
    ManagerListSerializer
)
from core.permissions import IsManager


@extend_schema_view(
    post=extend_schema(
        description='''Add a new manager.''',
        request=ManagerCreateSerializer,
        responses={
            '201': 'created',
            '400': 'Invalid data',
            '401': 'Unauthorized',
            '403': 'Permission denied for promoting managers',
        },
        tags=['Managers'],
    ),
)
class ManagerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanAddManager]
    serializer_class = ManagerCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@extend_schema_view(
    put=extend_schema(
        description='''Update a managers permissions.''',
        request=ManagerCreateSerializer,
        responses={
            '200': 'ok',
            '400': 'Invalid data',
            '401': 'Unauthorized',
            '403': 'Permission denied',
            '404': 'Manager not found',
        },
        tags=['Managers'],
    ),
    patch=extend_schema(
        description='''Update a managers permissions.''',
        request=ManagerCreateSerializer,
        responses={
            '200': 'ok',
            '400': 'Invalid data',
            '401': 'Unauthorized',
            '403': 'Permission denied',
            '404': 'Manager not found',
        },
        tags=['Managers'],
    ),
)
class ManagerUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, CanChangeManager]
    serializer_class = ManagerUpdateSerializer

    def get_object(self):
        manager = get_object_or_404(
            Manager,
            token=self.kwargs['manager_token']
        )
        self.check_object_permissions(self.request, manager)
        return manager


@extend_schema_view(
    delete=extend_schema(
        description='''Delete a manager.''',
        responses={
            '204': 'ok',
            '401': 'Unauthorized',
            '403': 'Permission denied for deleting managers',
            '404': 'Manager not found',
        },
        tags=['Managers'],
    ),
)
class ManagerDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, CanDeleteManager]

    def get_object(self):
        manager = get_object_or_404(
            Manager,
            token=self.kwargs['manager_token']
        )
        return manager


@extend_schema_view(
    get=extend_schema(
        description='''Retrieve a manager by admin/managers.''',
        responses={
            '200': 'ok',
            '401': 'Unauthorized',
            '403': 'Permission denied',
            '404': 'Manager not found',
        },
        tags=['Managers'],
    ),
)
class ManagerRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = ManagerRetrieveSerializer

    def get_object(self):
        manager = get_object_or_404(
            Manager,
            token=self.kwargs['manager_token']
        )
        return manager


@extend_schema_view(
    get=extend_schema(
        description='''List of managers.''',
        responses={
            '200': 'ok',
            '401': 'Unauthorized',
            '403': 'Permission denied',
        },
        tags=['Managers'],
    ),
)
class ManagerListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = ManagerListSerializer

    def get_queryset(self):
        return Manager.objects.all().order_by('-promotion_date')
