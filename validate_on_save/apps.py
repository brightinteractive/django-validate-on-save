from django.apps import AppConfig
import validate_on_save
from validate_on_save import django_allows_app_config

if django_allows_app_config():
    class ValidateOnSaveConfig(AppConfig):
        name = 'validate_on_save'

        def ready(self):
            validate_on_save.validate_models_on_save('validate_on_save')
