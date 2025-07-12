from django.apps import AppConfig

class BookclubprojectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookclubproject'

    def ready(self):
        from . import signals