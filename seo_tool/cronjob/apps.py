from django.apps import AppConfig
from django.conf import settings


class CronjobConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cronjob'

