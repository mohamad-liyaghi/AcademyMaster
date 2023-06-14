from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from managers.permissions import CanPromotePermission
from managers.serializers import ManagerCreateSerializer


@extend_schema_view(
    post=extend_schema(
        description='''Add a new manager.''',
        request=ManagerCreateSerializer,
        responses={
            '201': 'ok',
            '400': 'Invalid data',
        },
        tags=['Authentication'],
    ),
)
class ManagerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanPromotePermission]
    serializer_class = ManagerCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}
