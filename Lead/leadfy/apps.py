from django.apps import AppConfig


class LeadfyConfig(AppConfig):
    name = 'leadfy'

    def ready(self):
        import leadfy.signals
        # from jobs import updater
        # updater.start()
