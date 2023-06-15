from rest_framework import serializers
from typing import List
from managers.models import Manager, ManagerPermission
from django.contrib.auth.models import Permission
from rest_framework.exceptions import ValidationError


class BaseManagerSerializer(serializers.ModelSerializer):

    def _add_permissions(
            self,
            manager: Manager,
            permissions: List[ManagerPermission]
    ) -> None:
        '''Add permissions for a user'''
        if permissions:

            codenames = [permission.codename for permission in permissions]
            Manager.objects.add_permissions(
                user=manager.user,
                codenames=codenames
            )

    def _remove_all_permissions(self, manager: Manager) -> None:
        all_codenames = [permission.value for permission in ManagerPermission]
        Manager.objects.remove_permissions(
            user=manager.user,
            codenames=all_codenames
        )


class PermissionListQueryset(serializers.SlugRelatedField):
    def __init__(self, slug_field='codename', **kwargs):
        super().__init__(slug_field, **kwargs)

    def get_queryset(self):
        return Permission.objects.filter(
            codename__in=ManagerPermission
        ).select_related("content_type")


class ManagerCreateSerializer(BaseManagerSerializer):
    permissions = PermissionListQueryset(many=True, write_only=True)
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

        manager = Manager.objects.create(
            user=user,
            promoted_by=self.context['request'].user
        )

        # Add permissions for the use
        self._add_permissions(
            manager=manager,
            permissions=validated_data['permissions']
        )

        manager.save()
        return manager


class ManagerUpdateSerializer(BaseManagerSerializer):
    permissions = PermissionListQueryset(many=True, write_only=True)

    class Meta:
        model = Manager
        fields = ['permissions']

    def update(self, instance, validated_data):
        permissions = validated_data['permissions']
        self._update_permissions(instance, permissions)
        return super().update(instance, validated_data)

    def _update_permissions(self, instance, permissions):
        # Remove all user permissions
        self._remove_all_permissions(manager=instance)

        if permissions:
            # Add permissions if there are any.
            self._add_permissions(manager=instance, permissions=permissions)


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
        manager_permission_codenames = [
            permission.value for permission in ManagerPermission
        ]
        perms = value.user.user_permissions.filter(
            codename__in=manager_permission_codenames
        )

        serializer = ManagerPermissionListSerializer(perms, many=True)
        return serializer.data


class ManagerListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Manager
        fields = [
            'user',
            'token'
        ]
