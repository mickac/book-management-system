"""TODO:
    - PEP8 Validation + Doing some modules for repeating methods
    - Refactoring code (views to modules, Advanced Searching, Google API Fetch)
    - Unit tests
"""

import requests
import re

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .forms import BookForm
from .models import Book
from .serializers import BookSerializer
from .modules.book_operations import BookOperations
from .modules.errors import ErrorHandler
from .modules.paginator import paginator


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


def index(request):
    return render(request, 'index.html')


def book_add(request):
    template = 'book_add.html'
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                return BookOperations.book_add_or_edit(request, template, form)
            except Exception as exception:
                return ErrorHandler.generic_error(request, exception)
    else:
        form = BookForm()
    return render(request, template, {'form': form})


def book_list(request):
    template = 'book_list.html'
    try:
        book_list = Book.objects.all()
        page = request.GET.get('page', 1)
        pageSize = 5
        books = paginator(book_list, page, pageSize)
        return render(request, template, {'books': books})
    except Exception as exception:
        return ErrorHandler.generic_error(request, exception)


def book_edit(request, pk):
    template = 'book_edit.html'
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                return BookOperations.book_add_or_edit(request, template, form)
            except Exception as exception:
                return ErrorHandler.generic_error(request, exception)
    else:
        form = BookForm(instance=book)
    return render(request, template, {'form': form})


def book_search(request):
    template = 'book_search.html'
    try:
        keyword = request.GET.get('keyword')
        dateExact = request.GET.get('dateExact')
        dateFrom = request.GET.get('dateFrom')
        dateTo = request.GET.get('dateTo')
        parameter = request.GET.get('parameter')
        try:
            book_list = BookOperations.simple_search(request)
        except TypeError:
            return ErrorHandler.date_range_error(request, template)
        page = request.GET.get('page', 1)
        pageSize = 5
        books = paginator(book_list, page, pageSize)
        return render(request, template, {'books': books,
                                          'keyword': keyword,
                                          'dateExact': dateExact,
                                          'dateFrom': dateFrom,
                                          'dateTo': dateTo,
                                          'parameter': parameter})
    except Exception as exception:
        return ErrorHandler.generic_error(request, exception)


def book_advanced_searching(request):
    template = 'book_advanced_searching.html'
    if request.method == 'GET':
        if (len(request.GET) > 0):
            parameter = request.GET.get('parameter')
            dateParameter = request.GET.get('dateParameter')
            title = request.GET.get('title')
            authors = request.GET.get('authors')
            language = request.GET.get('language')
            isbnId = request.GET.get('isbnId')
            pageCount = request.GET.get('pageCount')
            exactDate = request.GET.get('exactDate')
            dateStart = request.GET.get('dateStart')
            dateEnd = request.GET.get('dateEnd')
            book_list = BookOperations.advanced_search(request)
            page = request.GET.get('page', 1)
            pageSize = 5
            books = paginator(book_list, page, pageSize)
            if (book_list.exists() == False):
                nobooks = True
                return render(request, template, { 'nobooks': nobooks,
                                                    'books': books})
            else:
                return render(request, template, { 'books': books,
                                                   'parameter':parameter,
                                                   'dateParameter':dateParameter,
                                                   'title': title,
                                                   'authors': authors,
                                                   'language': language,
                                                   'isbnId': isbnId,
                                                   'pageCount': pageCount,
                                                   'dateStart':dateStart,
                                                   'dateEnd': dateEnd, 
                                                   'exactDate': exactDate})
        else:
            return render(request, template)
    else:
        return render(request, template)


def feed_from_google(request):
    template = 'feed_from_google.html'
    resultNumbers = request.GET.get("resultNumbers")
    if request.method == 'GET' and resultNumbers:
        searchdict = request.GET.copy()
        q = request.GET.get("q")
        if("q" in searchdict):
            searchdict.pop("q")
        searchdict.pop("resultNumbers")    
        query = ""
        for x, y in searchdict.items():
            if x and y:
                query = query + "+" + x + ":" + y
        query = q + query + "&maxResults=" + resultNumbers + "&key=" + settings.GOOGLE_API_KEY
        if query:
            API_url = "https://www.googleapis.com/books/v1/volumes?q=" + query
        if (q == ""):
            API_url = API_url.replace("+", "", 1)
        API_url = API_url.replace(" ", "-")
        API_request = requests.get(API_url, headers={'Content-Type':'application/json'})
        data = API_request.json()
        addIter = 0
        isbn = isbnType = ""
        noItems = False
        print(API_url)
        if data.get("items"):
            for i in data.get("items"):
                title = i["volumeInfo"].get("title")
                authors = i["volumeInfo"].get("authors")
                publishedDate = i["volumeInfo"].get("publishedDate")
                if publishedDate and not re.findall("^\d\d\d\d[- /.]\d\d[- /.]\d\d$", publishedDate):
                    publishedDate = publishedDate + '-01-01'
                isbnId = i["volumeInfo"].get("industryIdentifiers")
                pageCount = i["volumeInfo"].get("pageCount")
                image = i["volumeInfo"].get("imageLinks")                    
                language = i["volumeInfo"].get("language")
                if title and authors and image and publishedDate and isbnId and pageCount and image and language:
                    if len(authors) > 1:
                        authors = ', '.join(authors)
                    else:
                        authors = authors[0]
                    image = image.get("thumbnail")
                    for j in isbnId:
                        if j["type"] == "ISBN_13":
                            isbn = j.get("identifier")
                            isbnType = "ISBN-13"
                        if j["type"] == "ISBN_10" and isbnType != "ISBN-13":
                            isbn = j.get("identifier")
                            isbnType = "ISBN-10"
                    if isbn:
                        book = Book(
                            title = title,
                            authors = authors,
                            publishedDate = publishedDate,
                            isbnType = isbnType,
                            isbnId = isbn,
                            pageCount = pageCount,
                            image = image,  
                            language = language
                        )
                        try:
                            book.save()
                            addIter += 1
                            noItems = False
                        except:
                            pass
        return render(request, template, {'addIter': addIter,'noItems': noItems})   
    else:
        return render(request, template)
