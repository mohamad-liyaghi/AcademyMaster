from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile
from profiles.serializers import ProfileUpdateSerializer
from profiles.permissions import IsProfileOwner


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
