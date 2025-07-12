from datetime import date as date
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.template import loader
from .models import Book

class AllBooks(ListView):
    model = Book
    template_name = 'bookclub/book_list.html'

class NewBooks(ListView):
    model = Book
    template_name = "bookclub/book_list.html"

    def get_queryset(self):
        return Book.objects.filter(published_date__gt=date.today() - timedelta(days=30))


def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    template = loader.get_template('bookclub/book_details.html')
    context = {
        'book': book,
    }
    return HttpResponse(template.render(context, request))