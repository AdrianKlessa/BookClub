from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    authors = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    avg_rating = models.FloatField(blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.title+" by "+self.authors