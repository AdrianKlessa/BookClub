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
    favorite_books = models.ManyToManyField(Book, related_name='favorited_by', blank=True)
    books_to_read = models.ManyToManyField(Book, related_name='added_to_reading_list_by', blank=True)

    def __str__(self):
        return self.user.username

class BookComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    published_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.user_profile.user.username+": "+self.comment

    def formatted_time(self):
        return self.published_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")