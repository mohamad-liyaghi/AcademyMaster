from managers.models import Manager
from core.permissions import IsManager


class CanAddManager(IsManager):
    """
    Only managers with can_promote perm can access the page
    """

    message = "You cannot promote managers."

    def has_permission(self, request, view):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Manager.get_permission("add")
        )


class CanDeleteManager(IsManager):
    """
    Only admins and managers with can_demote perm can access the page
    """

    message = "You cannot delete this manager."

    def has_permission(self, request, view):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Manager.get_permission("delete")
        )


class CanChangeManager(IsManager):
    """
    Only Manager with can_change perm can access the page
    """

    message = "You cannot update this manager."

    def has_object_permission(self, request, view, obj):
        return self._is_manager(request.user) and request.user.has_perm(
            perm_object=Manager.get_permission("change")
        )
