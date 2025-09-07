from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


    def ready(self):
        #import signals so post_migrate and post_save handlers are registered. 
        import users.signals
