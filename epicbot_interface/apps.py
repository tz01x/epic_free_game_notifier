from django.apps import AppConfig


class EpicbotInterfaceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "epicbot_interface"
    def ready(self) -> None:
        from .epic_bot.notify_user import get_active_promo_game
        get_active_promo_game()
        return super().ready()