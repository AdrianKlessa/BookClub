from django.contrib import admin

from bookclubproject.models import Book, Profile, BookComment

admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(BookComment)