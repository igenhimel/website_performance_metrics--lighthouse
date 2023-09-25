# models.py

from django.db import models

class PageScore(models.Model):
    performance_score = models.FloatField(null=True, blank=True)
    seo_score = models.FloatField(null=True, blank=True)
    best_practice_score = models.FloatField(null=True, blank=True)
    accessibility_score = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    

class JobExecutionLog(models.Model):
    job_name = models.CharField(max_length=255)
    start_message = models.TextField(blank=True, null=True)  # New field for start message
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now_add=True)
    
