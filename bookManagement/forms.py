from django import forms

from .models import Book

ISBN_TYPE_CHOICES = [
    ('10', 'ISBN 10'),
    ('13', 'ISBN 13'),
]
class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'title': 'Book title',
            'authors': 'Author(s)',
            'publishedDate': 'Date of publish',
            'isbnType': 'ISBN Type',
            'isbnId': 'ISBN ID',
            'pageCount': 'Number of pages',
            'image': 'URL of book cover',
        }