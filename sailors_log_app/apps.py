from django.apps import AppConfig


class SailorsLogAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sailors_log_app"

    def ready(self):
        import sailors_log_app.signals
