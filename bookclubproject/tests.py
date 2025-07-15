from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from bookclubproject.models import Book, User, Profile


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

class FavoritesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

    def test_add_to_favorites(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())

        url = reverse('add_to_favorites', args=[book1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_details', args=[book1.id]))

        profile = Profile.objects.get(user=self.user)
        self.assertIn(book1, profile.favorite_books.all())
        self.assertNotIn(book2, profile.favorite_books.all())

    def test_remove_from_favorites(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())
        book3 = create_book("Another book", date.today())

        profile = Profile.objects.get(user=self.user)
        profile.favorite_books.add(book1)
        profile.favorite_books.add(book2)

        url = reverse('remove_from_favorites', args=[book1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_details', args=[book1.id]))

        self.assertNotIn(book1, profile.favorite_books.all())
        self.assertIn(book2, profile.favorite_books.all())
        self.assertNotIn(book3, profile.favorite_books.all())

    def test_list_favorites(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())
        book3 = create_book("Another book", date.today())

        profile = Profile.objects.get(user=self.user)
        profile.favorite_books.add(book1)
        profile.favorite_books.add(book2)

        response = self.client.get(reverse("favorites"))
        self.assertEqual(list(response.context["book_list"]), [book1, book2])

class ReadingListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

    def test_add_to_reading_list(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())

        url = reverse('add_to_reading_list', args=[book1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_details', args=[book1.id]))

        profile = Profile.objects.get(user=self.user)
        self.assertIn(book1, profile.books_to_read.all())
        self.assertNotIn(book2, profile.books_to_read.all())

    def test_remove_from_reading_list(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())
        book3 = create_book("Another book", date.today())

        profile = Profile.objects.get(user=self.user)
        profile.books_to_read.add(book1)
        profile.books_to_read.add(book2)

        url = reverse('remove_from_reading_list', args=[book1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_details', args=[book1.id]))

        self.assertNotIn(book1, profile.books_to_read.all())
        self.assertIn(book2, profile.books_to_read.all())
        self.assertNotIn(book3, profile.books_to_read.all())

    def test_list_reading_list(self):
        book1 = create_book("Sherlock Holmes and XYZ", date.today())
        book2 = create_book("Sherlock Holmes and ZYX", date.today())
        book3 = create_book("Another book", date.today())

        profile = Profile.objects.get(user=self.user)
        profile.books_to_read.add(book1)
        profile.books_to_read.add(book2)

        response = self.client.get(reverse("reading_list"))
        self.assertEqual(list(response.context["book_list"]), [book1, book2])