from django.core.management.base import BaseCommand
from bookclubproject import models

class Command(BaseCommand):
    help = "Remove all books from database"

    def handle(self, *args, **options):
        models.Book.objects.all().delete()