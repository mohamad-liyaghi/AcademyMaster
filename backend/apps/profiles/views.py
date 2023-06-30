from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from profiles.models import Profile
from profiles.serializers import (
    ProfileUpdateSerializer,
    ProfileRetrieveSerializer
)
from profiles.permissions import IsProfileOwner, IsNonStudent


@extend_schema_view(
    put=extend_schema(
        description='''Update profile.''',
        request=ProfileUpdateSerializer,
        responses={
            '200': 'ok',
            '400': 'Invalid Data.',
            '401': 'User not authenticated.',
            '403': 'Attempting to update others profile.',
        },
        tags=['Profiles'],
    ),
    patch=extend_schema(
        description='''Update profile.''',
        request=ProfileUpdateSerializer,
        responses={
            '200': 'ok',
            '400': 'Invalid Data.',
            '401': 'User not authenticated.',
            '403': 'Attempting to update others profile.',
        },
        tags=['Profiles'],
    ),
)
class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]
    queryset = Profile.objects.all()

    def get_object(self):
        profile = get_object_or_404(
            Profile,
            token=self.kwargs.get('profile_token')
        )
        # Ensure profile owner is updating the profile
        self.check_object_permissions(self.request, profile)
        return profile


@extend_schema_view(
    get=extend_schema(
        description='''Retrieve a profile page by non-students.''',
        request=ProfileRetrieveSerializer,
        responses={
            '200': 'Success.',
            '401': 'User not authenticated.',
            '403': 'User is a student.',
            '404': 'Profile not found.',
        },
        tags=['Profiles'],
    ),
)
class ProfileRetrieveView(RetrieveAPIView):
    serializer_class = ProfileRetrieveSerializer
    permission_classes = [IsAuthenticated, IsNonStudent]

    def get_object(self):
        profile = get_object_or_404(
            Profile.objects.select_related('user'),
            token=self.kwargs.get('profile_token')
        )
        self.check_object_permissions(self.request, profile)
        return profile
