from django.apps import AppConfig


class GlobalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Global'

    def ready(self):
        import Global.signals