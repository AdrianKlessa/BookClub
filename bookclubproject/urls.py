from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllBooks.as_view(), name="index"),
    path("new", views.NewBooks.as_view(), name="new"),
    path("book_details/<int:id>", views.book_details, name="book_details"),
    path("book_search", views.BookSearchView.as_view(), name="book_search"),
    path("book_details/<int:id>/add_to_favorites/", views.add_to_favorites, name="add_to_favorites"),
    path("book_details/<int:id>/add_to_reading_list/", views.add_to_reading_list, name="add_to_reading_list"),
    path("book_details/<int:id>/remove_from_favorites/", views.remove_from_favorites, name="remove_from_favorites"),
    path("book_details/<int:id>/remove_from_reading_list/", views.remove_from_reading_list, name="remove_from_reading_list"),

    path("favorites", views.FavoriteBooks.as_view(), name="favorites"),
    path("reading_list", views.ReadingList.as_view(), name="reading_list"),
]