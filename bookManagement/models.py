from django.db import models

ISBN_TYPE_CHOICES = [
    ('10', 'ISBN 10'),
    ('13', 'ISBN 13'),
]

class Book(models.Model):
    title = models.CharField(max_length = 50)
    authors = models.CharField(max_length = 50)
    publishedDate = models.DateField()
    isbnType = models.CharField(max_length = 7, choices=ISBN_TYPE_CHOICES)
    isbnId = models.CharField(max_length = 13)
    pageCount = models.PositiveIntegerField()
    image = models.URLField()
    language = models.CharField(max_length = 50)