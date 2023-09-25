# models.py

from django.db import models

class PageScore(models.Model):
    performance_score = models.FloatField(null=True, blank=True)
    seo_score = models.FloatField(null=True, blank=True)
    best_practice_score = models.FloatField(null=True, blank=True)
    accessibility_score = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    
class LogMessage(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.created_at.strftime("%Y-%m-%d %H:%M:%S")