from django.db import models

class PageScore(models.Model):
    url = models.URLField(unique=True)
    first_contentful_paint = models.FloatField(null=True)  # Make other fields nullable as well if needed.
    largest_contentful_paint = models.FloatField(null=True)
    total_blocking_time = models.FloatField(null=True)
    seo_score = models.PositiveIntegerField(null=True)
    best_practice_score = models.PositiveIntegerField(null=True)
    accessibility_score = models.PositiveIntegerField(null=True)
    performance_score = models.PositiveIntegerField(null=True)
