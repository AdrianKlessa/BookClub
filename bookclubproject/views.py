from django.shortcuts import render
from django.views.generic import ListView

from .models import Book

class AllBooks(ListView):
    model = Book
    template_name = 'bookclub/index.html'
