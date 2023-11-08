from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from managers.models import Manager
from core.serializers import PermissionSerializer, UserProfileRelationSerializer


class ManagerCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="token", queryset=get_user_model().objects.all()
    )
    permissions = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Manager
        fields = ["user", "permissions", "token"]
        read_only_fields = ["token"]

    def create(self, validated_data):
        try:
            return Manager.objects.create_with_permissions(
                user=validated_data["user"],
                promoted_by=self.context["request"].user,
                codenames=validated_data.get("permissions", None),
            )

        except Exception as e:
            raise ValidationError(str(e))


class ManagerUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Manager
        fields = ["permissions"]

    def update(self, instance, validated_data):
        Manager.objects.update_permission(
            user=instance.user,
            permissions=[],
            codenames=validated_data.get("permissions", None),
        )
        return super().update(instance, validated_data)


class ManagerRetrieveSerializer(serializers.ModelSerializer):
    user = UserProfileRelationSerializer()
    # list of manager's permissions
    permissions = serializers.SerializerMethodField(method_name="get_permissions")

    class Meta:
        model = Manager
        fields = ["user", "promoted_by", "promotion_date", "permissions"]

    def get_permissions(self, value):
        permissions = Permission.objects.filter(user=value.user)
        return PermissionSerializer(permissions, many=True).data


class ManagerListSerializer(serializers.ModelSerializer):
    user = UserProfileRelationSerializer()

    class Meta:
        model = Manager
        fields = ["user", "token"]
