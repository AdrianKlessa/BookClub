from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllBooks.as_view(), name="index"),
    path("new", views.NewBooks.as_view(), name="new")
]