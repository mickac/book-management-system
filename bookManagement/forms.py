from django import forms

from .models import Book

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'authors', 'publishedDate', 'isbnType', 'isbnId', 'pageCount', 'image', 'language')