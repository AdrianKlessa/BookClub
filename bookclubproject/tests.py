from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from bookclubproject.models import Book

def create_book(title: str, published_date: date) -> Book:
    return Book.objects.create(title=title, published_date=published_date)

class NewBooksViewTest(TestCase):

    def test_only_new_books(self):
        new_books = []
        old_books = []
        for i in range(30):
            new_books.append(create_book("Today's Book", date.today()))
        for i in range(30):
            old_books.append(create_book("Old Book", date.today() - timedelta(days=365)))
        response = self.client.get(reverse("new"))
        self.assertEqual(list(response.context["book_list"]), new_books)