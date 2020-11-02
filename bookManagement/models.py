from django.db import models

class Book(models.Model):
    title = models.CharField(max_length = 50)
    authors = models.CharField(max_length = 50)
    publishedDate = models.DateField()
    isbnType = models.CharField(max_length = 7)
    isbnId = models.CharField(max_length = 13)
    pageCount = models.PositiveIntegerField()
    image = models.URLField()
    language = models.CharField(max_length = 50)