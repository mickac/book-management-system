from django.db import models

ISBN_TYPE_CHOICES = [
    ('ISBN-10', 'ISBN-10'),
    ('ISBN-13', 'ISBN-13'),
]


class Book(models.Model):
    title = models.CharField(max_length = 50)
    authors = models.CharField(max_length = 50)
    publishedDate = models.DateField(help_text = "Use 'yyyy-mm-dd' date format. For example '2020-10-30'.")
    isbnType = models.CharField(max_length = 7, 
                                choices = ISBN_TYPE_CHOICES, 
                                help_text = "Choose type of ISBN normalization you want to use.")
    isbnId = models.CharField(max_length = 17, 
                              help_text = """
                                            Insert ISBN ID compatible with type you have chosen. 
                                            For example (for ISBN-13): 978-2-1234-5680-3 or 9782123456803.")
                                          """,
                              unique=True)
    pageCount = models.PositiveIntegerField()
    image = models.URLField()
    language = models.CharField(max_length = 50)


    def __str__(self):
        return self.title