from django.db import models
from django.core.cache import cache


class AccountRole(models.Model):
    """
    This model is responsible for user roles
    is_admin() -> Check user is admin (superuser)
    is_manager() -> Check user has Manager object
    is_teacher() -> Check user has Teacher Object
    is_student() -> Check user is non of admin/manager/teacher
    _get_chached_role() -> Check the cache to see users role
    _set_cached_role() -> Set user role in cache for 10 seconds

    """

    class Meta:
        abstract = True

    def is_admin(self) -> bool:
        """Check user is admin or not"""

        # First check in cache
        if self._get_cached_role("admin"):
            return True

        if self.is_staff:
            # Set in cache
            self._set_cached_role("admin")
            return True

        return False

    def is_manager(self) -> bool:
        """
        Check user is manager or not.
        Admins also have manager permissions
        """
        # First check in cache
        if self._get_cached_role("manager", "admin"):
            return True

        if self.is_admin():
            return True

        try:
            # Check user has 1 to 1 rel with any manager obj
            if self.manager.id:
                self._set_cached_role("manager")
                return True
        except Exception:
            return False

    def is_teacher(self) -> bool:
        """
        Check user is teacher or not
        Admins have teachers permissions as well
        """
        if self._get_cached_role("teacher", "admin"):
            return True

        if self.is_admin():
            return True

        try:
            # Check user has 1 to 1 rel with any teacher obj
            if self.teacher.id:
                self._set_cached_role("teacher")
                return True

        except Exception:
            return False

    def is_student(self) -> bool:
        """Check user is not admin/manager or teacher."""

        if self._get_cached_role("student"):
            return True

        if not self.is_admin() and not self.is_manager() and not self.is_teacher():
            # Set in cache
            self._set_cached_role("student")
            return True

        return False

    def _get_cached_role(self, *roles) -> bool:
        """Get user role from cache and compare with given roles"""
        cached_role = cache.get(f"role:{self.token}")
        return cached_role and cached_role in roles

    def _set_cached_role(self, role: str) -> None:
        """Set role for user in cache for 10 seconds"""
        cache.set(f"role:{self.token}", role, 10)
