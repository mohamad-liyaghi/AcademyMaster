from django.apps import AppConfig


class EnrollmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enrollments'

    def ready(self) -> None:
        import enrollments.signals
