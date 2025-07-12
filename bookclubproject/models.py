from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    favorite_books = models.ManyToManyField(Book, related_name='favorited_by')
    books_to_read = models.ManyToManyField(Book, related_name='added_to_reading_list_by')
    def __str__(self):
        return self.user.username