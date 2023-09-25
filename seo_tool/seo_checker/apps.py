from django.apps import AppConfig
from django.conf import settings

class SeoCheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seo_checker'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from seo_tool import operator
            operator.start()
