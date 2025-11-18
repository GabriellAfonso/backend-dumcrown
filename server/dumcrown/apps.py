from django.apps import AppConfig


class DumcrownConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dumcrown'

    def ready(self) -> None:
        import dumcrown.signals as _
