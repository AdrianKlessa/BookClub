from datetime import date as date
from datetime import timedelta
from django.shortcuts import render
from django.views.generic import ListView

from .models import Book

class AllBooks(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'

class NewBooks(ListView):
    model = Book
    template_name = "bookclub/book_list.html"

    def get_queryset(self):
        return Book.objects.filter(published_date__gt=date.today() - timedelta(days=30))