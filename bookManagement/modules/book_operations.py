from django.shortcuts import render

from .validators import IsbnValidator
from .errors import ErrorHandler


class BookOperations:
    def book_add_or_edit(request, template, form):
        """Taking parameters from form and adding or editing book"""
        isbnType = form.cleaned_data['isbnType']
        isbnId = form.cleaned_data['isbnId']
        title = form.cleaned_data['title']
        try:
            IsbnValidator.validate_dashes(isbnType, isbnId)
            IsbnValidator.validate_isbn_len(isbnType, isbnId)
        except ValueError:
            return ErrorHandler.isbn_validation_error(request, template, form)
        else:
            book = form.save(commit=False)
            book.isbnId = isbnId.replace("-", "")
            book.save()
            return render(request, template, {'title': title,
                                              'form': form})
