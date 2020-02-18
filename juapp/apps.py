from django.apps import AppConfig


class JuappConfig(AppConfig):
    name = 'juapp'

    def ready(self):
        from diarioUpdater import updater
        updater.start()