from django.apps import AppConfig
from django.conf import settings
import os

class EpicbotInterfaceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "epicbot_interface"
    def ready(self) -> None:
        
        from epicbot_interface.schedulars import Schedular
    
        if settings.IS_RUNSERVER \
            or os.getenv('START_BACKGROUND','FALSE') == 'TRUE':
    
            Schedular.start()
        
        return super().ready()