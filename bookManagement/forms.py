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


class AdvancedSearch(forms.Form):
    title = forms.CharField(max_length = 50, required=False)
    authors = forms.CharField(max_length = 50, required=False)
    dateStart = forms.DateField(required=False)
    dateEnd = forms.DateField(required=False)
    exactDate = forms.DateField(required=False)
    isbnId = forms.CharField(required=False)
    pageCount = forms.IntegerField(required=False)
    language = forms.CharField(max_length = 50, required=False)