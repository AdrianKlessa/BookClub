from datetime import date as date
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.template import loader
from .models import Book, Profile

class AllBooks(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'

class NewBooks(ListView):
    model = Book
    template_name = "bookclub/book_list.html"

    def get_queryset(self):
        return Book.objects.order_by("-published_date")[:30]

class BookSearchView(ListView):
    model = Book
    template_name = "bookclub/book_search.html"

    def get_queryset(self):
        result = super(BookSearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Book.objects.filter(title__contains=query)
            result = postresult
        else:
            result = None
        return result

def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    template = loader.get_template('bookclub/book_details.html')
    context = {
        'book': book,
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_to_favorites(request, id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=id)
        profile, created = Profile.objects.get_or_create(user=request.user)
        if book not in profile.favorite_books.all():
            profile.favorite_books.add(book)
    return redirect('book_details', id=id)

@login_required
def add_to_reading_list(request, id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=id)
        profile, created = Profile.objects.get_or_create(user=request.user)
        if book not in profile.books_to_read.all():
            profile.books_to_read.add(book)
    return redirect('book_details', id=id)