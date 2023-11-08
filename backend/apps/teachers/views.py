from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from teachers.permissions import (
    CanAddTeacher,
    CanDeleteTeacher,
    CanUpdateTeacher,
)
from teachers.serializers import (
    TeacherCreateSerializer,
    TeacherRetrieveSerializer,
    TeacherUpdateSerializer,
    TeacherListSerializer,
)
from teachers.models import Teacher


@extend_schema_view(
    post=extend_schema(
        description="""Create a new teacher by admin/managers.""",
        request=TeacherCreateSerializer,
        responses={
            "201": "ok",
            "400": "Invalid data",
            "401": "Unauthorized",
            "403": "Permission denied for adding teachers",
        },
        tags=["Teachers"],
    ),
)
class TeacherCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, CanAddTeacher]
    serializer_class = TeacherCreateSerializer

    def get_serializer_context(self):
        return {"request": self.request}


@extend_schema_view(
    get=extend_schema(
        description="""Retrieve a teacher.""",
        request=TeacherRetrieveSerializer,
        responses={
            "200": "ok",
            "401": "Unauthorized",
            "404": "Not found",
        },
        tags=["Teachers"],
    ),
)
class TeacherRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherRetrieveSerializer

    def get_object(self):
        return get_object_or_404(
            Teacher.objects.select_related("user", "user__profile"),
            token=self.kwargs["teacher_token"],
        )


@extend_schema_view(
    put=extend_schema(
        description="""Update teacher contact links/description.""",
        request=TeacherUpdateSerializer,
        responses={
            "200": "ok",
            "401": "Unauthorized",
            "403": "Permission denied for updating teachers",
            "404": "Not found",
        },
        tags=["Teachers"],
    ),
    patch=extend_schema(
        description="""Update teacher contact links/description.""",
        request=TeacherUpdateSerializer,
        responses={
            "200": "ok",
            "401": "Unauthorized",
            "403": "Permission denied for updating teachers",
            "404": "Not found",
        },
        tags=["Teachers"],
    ),
)
class TeacherUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, CanUpdateTeacher]
    serializer_class = TeacherUpdateSerializer

    def get_object(self):
        teacher = get_object_or_404(
            Teacher.objects.select_related("user"), token=self.kwargs["teacher_token"]
        )
        self.check_object_permissions(self.request, teacher)
        return teacher


@extend_schema_view(
    delete=extend_schema(
        description="""Delete a teacher only by manager/admins.""",
        responses={
            "204": "ok",
            "401": "Unauthorized",
            "403": "Permission denied for deleting teachers",
            "404": "Not found",
        },
        tags=["Teachers"],
    ),
)
class TeacherDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, CanDeleteTeacher]

    def get_object(self):
        teacher = get_object_or_404(
            Teacher.objects.select_related("user"), token=self.kwargs["teacher_token"]
        )
        return teacher


@extend_schema_view(
    get=extend_schema(
        description="""List of teachers all.""",
        responses={
            "200": "ok",
            "401": "Unauthorized",
        },
        tags=["Teachers"],
    ),
)
class TeacherListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherListSerializer

    def get_queryset(self):
        return (
            Teacher.objects.select_related("user", "user__profile")
            .all()
            .order_by("-promotion_date")
        )
