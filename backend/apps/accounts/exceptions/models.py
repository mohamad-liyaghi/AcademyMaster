from django.core.exceptions import ValidationError


class DuplicationCodeException(ValidationError):
    """
    Raise when user has an active code and tempting to create new one
    """

    pass


class ActiveUserCodeException(ValidationError):
    """Raise when active user tempting to create new code"""

    pass
