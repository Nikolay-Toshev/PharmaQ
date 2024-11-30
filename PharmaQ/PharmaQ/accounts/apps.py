from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PharmaQ.accounts'

    def ready(self):
        import PharmaQ.accounts.signals