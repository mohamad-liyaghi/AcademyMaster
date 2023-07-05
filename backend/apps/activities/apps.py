from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activities'

    def ready(self) -> None:
        import activities.signals
