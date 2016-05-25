from __future__ import unicode_literals

from django.apps import AppConfig


class EscapadConfig(AppConfig):
    name = 'escapad'
    
    def ready(self):
        # import signal handlers
        import escapad.signals