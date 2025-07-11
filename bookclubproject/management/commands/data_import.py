import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from bookclubproject import models

# Load the dataset from https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks as an example

class Command(BaseCommand):
    help = "Load the data from books.csv"

    def handle(self, *args, **options):
        with open("books.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            date_format = "%m/%d/%Y"
            next(reader, None) # Skip header
            books = []
            for row in reader:
                # skip bad lines
                if len(row)!=12:
                    continue
                try:
                    pub_date = datetime.datetime.strptime(row[10], date_format).date()
                except ValueError:
                    continue
                new_book = models.Book(
                    title=row[1],
                    authors=row[2],
                    description="N/A",
                    avg_rating=row[3],
                    isbn=row[4],
                    published_date=pub_date,
                    publisher=row[10]
                )
                books.append(new_book)
        models.Book.objects.bulk_create(books)