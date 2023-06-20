from rest_framework import serializers
from django.contrib.auth.models import Permission
from rest_framework.exceptions import ValidationError
from managers.models import Manager


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['codename']


class ManagerCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    token = serializers.CharField(read_only=True)

    class Meta:
        model = Manager
        fields = ['user', 'permissions', 'token']

    def create(self, validated_data):
        user = validated_data['user']

        if user.is_admin():
            raise ValidationError('Admins cannot become managers.')

        if user.is_manager():
            raise ValidationError('User is already a manager.')

        manager = Manager.objects.create_with_permissions(
            user=user,
            promoted_by=self.context['request'].user,
            codenames=validated_data.get('permissions', None),
        )

        return manager


class ManagerUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Manager
        fields = ['permissions']

    def update(self, instance, validated_data):
        Manager.objects.update_permission(
                user=instance.user,
                permissions=[],
                codenames=validated_data.get('permissions', None)
        )
        return super().update(instance, validated_data)


class ManagerRetrieveSerializer(serializers.ModelSerializer):
    # list of manager's permissions
    permissions = serializers.SerializerMethodField(
        method_name='get_permissions'
    )

    class Meta:
        model = Manager
        fields = [
            'user',
            'promoted_by',
            'promotion_date',
            'permissions'
        ]

    def get_permissions(self, value):
        permissions = Permission.objects.filter(
            user=value.user,
        )

        serializer = PermissionSerializer(permissions, many=True)
        return serializer.data


class ManagerListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Manager
        fields = [
            'user',
            'token'
        ]
