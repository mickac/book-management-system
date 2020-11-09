import datetime as dt
import requests

from django.shortcuts import render
from django.db.models import Q

from .api_operations import operationsAPI
from .validators import IsbnValidator
from .errors import ErrorHandler
from ..models import Book


class BookOperations:
    def __init__(self, request):
        self.request = request

    def book_add_or_edit(self, template, form):
        """Taking parameters from form and adding or editing book."""
        isbnType = form.cleaned_data['isbnType']
        isbnId = form.cleaned_data['isbnId']
        title = form.cleaned_data['title']
        try:
            IsbnValidator(isbnType, isbnId).validate_dashes()
            IsbnValidator(isbnType, isbnId).validate_isbn_len()
        except ValueError:
            return ErrorHandler.isbn_validation_error(self.request,
                                                      template, form)
        else:
            book = form.save(commit=False)
            book.isbnId = isbnId.replace("-", "")
            book.save()
            return render(self.request, template, {'title': title,
                                                   'form': form})

    def simple_search(self):
        """Preparing data for simple search."""
        parameter = self.request.GET.get('parameter')
        if parameter == 'dateRange':
            targetword = [str(self.request.GET.get('dateFrom')),
                          str(self.request.GET.get('dateTo'))]
            searchword = "publishedDate__range"
        elif parameter == 'publishedDate':
            targetword = str(self.request.GET.get('dateExact'))
            searchword = "publishedDate__exact"
        else:
            targetword = self.request.GET.get('keyword')
            searchword = parameter + "__icontains"
        filtered_list = Book.objects.filter(
            Q(**{searchword: targetword})
        )
        return filtered_list

    def advanced_search(self):
        searchdict = self.request.GET.copy()
        searchdict["publishedDate"] = self.request.GET.get('exactDate')
        searchdict.pop("exactDate")
        advanced_filter = Q()
        if searchdict["parameter"] == '1':
            """ If user choose "Contain any fields" algoritm do following things:
                1. Deleting "page" and "date parameter" from dictionary so
                    advanced_filter doesn't check those keys
                    and values in DB (causing errors).
                2. If published date is empty it's giving it some random,
                    irrelevant value so advanced_filter
                    doesn't fails in DB searching.
                3. If there are not date for range it's deleting
                    those keys and valuse from dictionary so
                    advanced_filter can skip them in searching.
                4. If there is one date from range it's either gives
                    dateEnd current date or dateStart some very futher date.
            """
            searchdict.pop("parameter")
            if "dateParameter" in searchdict:
                searchdict.pop("dateParameter")
            if "page" in searchdict:
                searchdict.pop("page")
            if not searchdict.get("publishedDate"):
                searchdict["publishedDate"] = "1000-01-01"
            if searchdict["dateStart"] and not searchdict["dateEnd"]:
                searchdict["publishedDate__range"] = [searchdict["dateStart"],
                                                      str(dt.datetime.now())]
            if not searchdict["dateStart"] and searchdict["dateEnd"]:
                searchdict["publishedDate__range"] = ["1000-01-01",
                                                      searchdict["dateEnd"]]
            if searchdict["dateStart"] and searchdict["dateEnd"]:
                searchdict["publishedDate__range"] = [searchdict["dateStart"],
                                                      searchdict["dateEnd"]]
            searchdict.pop("dateStart")
            searchdict.pop("dateEnd")
            for searchword in searchdict:
                advanced_filter |= Q(**{searchword: searchdict[searchword]})
        elif searchdict["parameter"] == '2':
            """If user choose "Contain all fields" algorithm do following things.
                Because all fields are required, depending what
                date parameter user choose algorithm either deletes
                publishedDate and after giving range values
                to new variable it's deleting ranges too or just
                deleting ranges and leaves publishedDate
                parameter for exact date searching.
            """
            searchdict.pop("parameter")
            if searchdict["dateParameter"] == '1':
                searchdict["publishedDate__range"] = [searchdict["dateStart"],
                                                      searchdict["dateEnd"]]
                searchdict.pop("publishedDate")
            searchdict.pop("dateStart")
            searchdict.pop("dateEnd")
            searchdict.pop("dateParameter")
            for searchword in searchdict:
                advanced_filter &= Q(**{searchword: searchdict[searchword]})
        return Book.objects.filter(advanced_filter)

    def import_from_google_api(self):
        API_url = operationsAPI.create_query(self.request)
        API_request = requests.get(API_url, headers={'Content-Type':
                                                     'application/json'})
        data = API_request.json()
        return operationsAPI.unpack_and_add(data)
