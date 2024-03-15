from django.apps import AppConfig


class FosscellConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fosscell'

    def ready(self):
        import fosscell.signals