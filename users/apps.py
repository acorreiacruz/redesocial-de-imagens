from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self, *args, **kwargs) -> None:
        from users import signals
        return super().ready(*args, **kwargs)
