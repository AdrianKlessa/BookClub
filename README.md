### A Django web app for keeping up with books you want to read and discussing them with others

![Test workflow](https://github.com/AdrianKlessa/BookClub/actions/workflows/django.yml/badge.svg)

For testing the application I've used [this dataset](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks) from Kaggle. 
To import data simply place `books.csv` at the root of the project (alongside `manage.py` and this readme) and then run `data_import` from the Django shell (it'll use the included script). 