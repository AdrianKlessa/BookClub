from django.apps import AppConfig

class BookclubprojectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookclubproject'


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import signals