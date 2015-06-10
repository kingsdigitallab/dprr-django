from django.apps import AppConfig

class PRomRepConfig(AppConfig):
    name = 'promrep'

    def ready(self):
        import promrep.signals