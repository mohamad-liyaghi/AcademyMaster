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
        ),
        write_only=True
    )

    class Meta:
        model = Manager
        fields = ['user', 'permissions']

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

        if validated_data['permissions']:
            codenames = [permission.codename for permission
                         in validated_data['permissions']]
            Manager.objects.add_permissions(
                user=manager.user,
                codenames=[*codenames]
            )

        manager.save()
        return manager
