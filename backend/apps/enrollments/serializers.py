from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Enrollment
from courses.models import Course
from core.serializers import CourseRelationSerializer, UserProfileRelationSerializer


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field="token", queryset=Course.objects.only("token")
    )
    user = serializers.StringRelatedField()

    class Meta:
        model = Enrollment
        fields = ("course", "user", "status", "created_at")
        read_only_fields = ("status", "created_at", "user")

    def create(self, validated_data):
        validated_data.update({"user": self.context["request"].user})
        try:
            return Enrollment.objects.create(**validated_data)
        except Exception as e:
            raise ValidationError(str(e))


class EnrollmentRetrieveSerializer(serializers.ModelSerializer):
    course = CourseRelationSerializer()
    user = UserProfileRelationSerializer()

    class Meta:
        model = Enrollment
        fields = ("course", "user", "status", "created_at")
        read_only_fields = ("course", "user", "status", "created_at")


class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ("status", "created_at")
        read_only_fields = ("created_at",)


class EnrollmentListSerializer(serializers.ModelSerializer):
    course = CourseRelationSerializer()
    user = UserProfileRelationSerializer()

    class Meta:
        model = Enrollment
        fields = ("user", "course", "get_status_display", "created_at", "token")
        read_only_fields = fields
