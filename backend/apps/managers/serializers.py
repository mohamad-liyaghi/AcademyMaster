from rest_framework import serializers
from managers.models import Manager, ManagerPermission
from django.contrib.auth.models import Permission
from rest_framework.exceptions import ValidationError


class ManagerCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        slug_field='codename',
        queryset=Permission.objects.filter(
            codename__in=ManagerPermission
        ).select_related("content_type"),
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

        manager = Manager.objects.create(
            user=user,
            promoted_by=self.context['request'].user
        )

        self._add_permissions(manager, validated_data['permissions'])

        manager.save()
        return manager

    def _add_permissions(self, manager, permissions):
        if permissions:
            codenames = [permission.codename for permission in permissions]
            Manager.objects.add_permissions(
                user=manager.user,
                codenames=codenames
            )


class ManagerUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        slug_field='codename',
        queryset=Permission.objects.filter(
            codename__in=ManagerPermission
        ).select_related("content_type"),
        write_only=True
    )

    class Meta:
        model = Manager
        fields = ['permissions']

    def update(self, instance, validated_data):
        permissions = validated_data['permissions']
        self._update_permissions(instance, permissions)

        return super().update(instance, validated_data)

    def _update_permissions(self, instance, permissions):
        all_codenames = [permission.value for permission in ManagerPermission]
        # Remove all permissions first
        Manager.objects.remove_permissions(
            user=instance.user,
            codenames=all_codenames
        )

        if permissions:
            requested_codenames = [
                permission.codename for permission in permissions
            ]
            Manager.objects.add_permissions(
                user=instance.user,
                codenames=requested_codenames
            )


class ManagerPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name']


class ManagerRetrieveSerializer(serializers.ModelSerializer):
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
        all_codenames = [permission.value for permission in ManagerPermission]
        perms = value.user.user_permissions.filter(codename__in=all_codenames)

        serializer = ManagerPermissionSerializer(perms, many=True)
        return serializer.data
