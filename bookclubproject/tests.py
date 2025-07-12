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

class BookSearchViewTest(TestCase):
    def test_search_contains(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())
        book3 = create_book("Another book", date.today())

        response = self.client.get(reverse('book_search') + '?search=Holmes')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        books = response.context['book_list']
        self.assertIn(book1, books)
        self.assertIn(book2, books)
        self.assertNotIn(book3, books)

    def test_search_case_insensitive(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())
        book3 = create_book("Another book", date.today())

        response = self.client.get(reverse('book_search') + '?search=holmes')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        books = response.context['book_list']
        self.assertIn(book1, books)
        self.assertIn(book2, books)
        self.assertNotIn(book3, books)