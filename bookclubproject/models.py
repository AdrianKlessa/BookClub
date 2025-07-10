from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    authors = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    avg_rating = models.FloatField()
    published_date = models.DateField()
    isbn = models.CharField(max_length=15)

    def __str__(self):
        return self.title+" by "+self.authors