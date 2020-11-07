from django import forms

from .models import Book


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
