from datetime import date as date
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.template import loader
from .models import Book, Profile, BookComment
from .forms import BookCommentForm
from django.db.models import Q

class AllBooks(ListView):
    model = Book
    template_name = 'bookclub/all_books.html'

class NewBooks(ListView):
    model = Book
    template_name = "bookclub/new_books.html"

    def get_queryset(self):
        return Book.objects.order_by("-published_date")[:30]

class FavoriteBooks(ListView):
    model = Book
    template_name = "bookclub/favorites.html"

    def get_queryset(self):
        return Profile.objects.get_or_create(user=self.request.user)[0].favorite_books.all()

class ReadingList(ListView):
    model = Book
    template_name = "bookclub/reading_list.html"

    def get_queryset(self):
        return Profile.objects.get_or_create(user=self.request.user)[0].books_to_read.all()

class BookSearchView(ListView):
    model = Book
    template_name = "bookclub/book_search.html"

    def get_queryset(self):
        result = super(BookSearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Book.objects.filter(Q(title__icontains=query) | Q(authors__icontains=query))
            result = postresult
        else:
            result = None
        return result

def book_details(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        form = BookCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            user_profile, created = Profile.objects.get_or_create(user=request.user)
            comment.user_profile = user_profile
            comment.book = book
            comment.save()
            return redirect('book_details', id=id)

    comment_form = BookCommentForm()
    comments = BookComment.objects.filter(book=book).order_by('-published_datetime').all()
    template = loader.get_template('bookclub/book_details.html')
    context = {
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
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
def remove_from_favorites(request, id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=id)
        profile, created = Profile.objects.get_or_create(user=request.user)
        if book in profile.favorite_books.all():
            profile.favorite_books.remove(book)
    return redirect('book_details', id=id)

@login_required
def add_to_reading_list(request, id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=id)
        profile, created = Profile.objects.get_or_create(user=request.user)
        if book not in profile.books_to_read.all():
            profile.books_to_read.add(book)
    return redirect('book_details', id=id)

@login_required
def remove_from_reading_list(request, id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=id)
        profile, created = Profile.objects.get_or_create(user=request.user)
        if book in profile.books_to_read.all():
            profile.books_to_read.remove(book)
    return redirect('book_details', id=id)
