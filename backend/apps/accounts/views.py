from rest_framework.generics import CreateAPIView
from accounts.serializers import AccountRegisterSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    post=extend_schema(
        description='''Register a new user.''',
        request=AccountRegisterSerializer,
        tags=['Authentication'],
    ),
)
class UserRegisterView(CreateAPIView):
    serializer_class = AccountRegisterSerializer
