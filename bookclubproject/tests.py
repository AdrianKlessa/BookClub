from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from bookclubproject.models import Book

def create_book(title: str, published_date: date) -> Book:
    return Book.objects.create(title=title, published_date=published_date)

class NewBooksViewTest(TestCase):

    def test_todays_book(self):
        book = create_book("Today's Book", date.today())
        response = self.client.get(reverse("new"))
        self.assertEqual(list(response.context["book_list"]), [book])

    def test_old_book(self):
        book = create_book("Old Book", date.today()-timedelta(days=365))
        response = self.client.get(reverse("new"))
        self.assertEqual(list(response.context["book_list"]), [])