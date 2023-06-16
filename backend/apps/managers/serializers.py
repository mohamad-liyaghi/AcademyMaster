from rest_framework import serializers
from managers.models import Manager, ManagerPermission
from django.contrib.auth.models import Permission
from rest_framework.exceptions import ValidationError


class ManagerCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.MultipleChoiceField(
        choices=ManagerPermission.choices,
        write_only=True
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
            permissions=validated_data['permissions'],
        )

        return manager


class ManagerUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.MultipleChoiceField(
        choices=ManagerPermission.choices,
        write_only=True
    )

    class Meta:
        model = Manager
        fields = ['permissions']

    def update(self, instance, validated_data):
        Manager.objects.update_permission(
                user=instance.user,
                permissions=validated_data['permissions']
        )
        return super().update(instance, validated_data)


class ManagerPermissionListSerializer(serializers.ModelSerializer):
    '''List of a managers permissions'''
    class Meta:
        model = Permission
        fields = ['name']


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
        permissions = Manager.objects.get_permission_list(
            user=value.user,
            permission_class=ManagerPermission
        )

        serializer = ManagerPermissionListSerializer(permissions, many=True)
        return serializer.data


class ManagerListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Manager
        fields = [
            'user',
            'token'
        ]
