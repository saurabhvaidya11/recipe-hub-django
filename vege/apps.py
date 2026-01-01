from django.apps import AppConfig


class VegeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vege'
    
    
def ready(self):
    import your_app.signals

