from django.apps import AppConfig


class LoarnConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "config.apps.Loan"

    def ready(self):
        from . import signals

        print(signals)
