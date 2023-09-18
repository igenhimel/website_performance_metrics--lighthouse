from django.db import models

class PageScore(models.Model):
    performance_score = models.FloatField(null=True)
    seo_score = models.FloatField(null=True)
    best_practice_score = models.FloatField(null=True)
    accessibility_score = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__ (self):
        return f'Scores for page (ID: {self.pk})'