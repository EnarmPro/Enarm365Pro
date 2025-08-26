from django.apps import AppConfig # pyright: ignore[reportMissingModuleSource]


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
