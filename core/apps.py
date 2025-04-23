# core/apps.py

from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'            # já existente
    verbose_name = "Core"

    def ready(self):
        # aqui dentro você importa o módulo onde estão os seus signals
        import core.signals
