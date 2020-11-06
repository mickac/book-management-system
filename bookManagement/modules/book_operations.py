import datetime

from django.shortcuts import render
from django.db.models import Q

from .validators import IsbnValidator
from .errors import ErrorHandler
from ..models import Book


class BookOperations:
    def book_add_or_edit(request, template, form):
        """Taking parameters from form and adding or editing book."""
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

    def simple_search(request):
        """Preparing data for simple search."""
        parameter = request.GET.get('parameter')
        if parameter == 'dateRange':
            targetword = [str(request.GET.get('dateFrom')),
                          str(request.GET.get('dateTo'))]
            searchword = "publishedDate__range"
        elif parameter == 'publishedDate':
            targetword = str(request.GET.get('dateExact'))
            searchword = "publishedDate__exact"
        else:
            targetword = request.GET.get('keyword')
            searchword = parameter + "__icontains"
        filtered_list = Book.objects.filter(
            Q(**{searchword: targetword})
        )
        return filtered_list

    def advanced_search(request, template):
        parameter = request.GET.get('parameter')
        dateStart = request.GET.get('dateStart')
        dateEnd = request.GET.get('dateEnd')
        searchdict = request.GET.copy()
        searchdict.pop("exactDate")
        searchdict.pop("parameter")
        searchdict["publishedDate"] = request.GET.get('exactDate')
        advanced_filter = Q()
        if(parameter == '1'):
            if("page" in searchdict):
                searchdict.pop("page")
            if(not searchdict.get("publishedDate")):
                searchdict["publishedDate"] = "1000-01-01"
            if(not searchdict.get("pageCount")):
                searchdict["pageCount"] = 0
            if(not searchdict["dateStart"] and not searchdict["dateEnd"]):
                searchdict.pop("dateStart")
                searchdict.pop("dateEnd")
            elif(searchdict["dateStart"] and not searchdict["dateEnd"]):
                searchdict["dateEnd"] = datetime.datetime.now()
            elif(not searchdict["dateStart"] and searchdict["dateEnd"]):
                searchdict["dateStart"] = "1000-01-01"
            for searchword in searchdict:
                advanced_filter |= Q(**{searchword:searchdict[searchword]})
        elif (parameter == '2'):
            emptyFieldsCounter = list(filter(lambda x: x == '',(list(searchdict.values())))).count('')
            if(not searchdict["dateStart"] and not searchdict["dateEnd"] and emptyFieldsCounter == 2):
                searchdict.pop("dateStart")
                searchdict.pop("dateEnd")
            elif(not searchdict["publishedDate"] and emptyFieldsCounter == 1):
                searchdict.pop("publishedDate")
                searchdict.pop("dateStart")
                searchdict.pop("dateEnd")
                searchdict["publishedDate__range"] = [str(dateStart), str(dateEnd)]
            elif(emptyFieldsCounter > 2):
                error = 'You are missing some field(s). Please fill them!'
                return render(request, template, {'error': error})
            else:
                error = 'Use "Exact date" OR "Date from, Date to" for contains all field!'
                return render(request, template, {'error': error})
            for searchword in searchdict:
                advanced_filter &= Q(**{searchword:searchdict[searchword]})   
        return Book.objects.filter(advanced_filter)