"""TODO:
    - PEP8 Validation + Doing some modules for repeating methods
    - Feed from Google API (halfway done, accidentely reached API limits)
"""

import datetime
import requests
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404, request, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .forms import BookForm
from .models import Book
from .serializers import BookSerializer
from .modules.paginator import paginator
from .modules.validators import(
    validate_dashes,
    validate_isbn_len
)
from .modules.errors import(
    generic_error,
    isbn_validation_error,
    date_error
)

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
                isbnType = form.cleaned_data['isbnType']
                isbnId = form.cleaned_data['isbnId']
                title = form.cleaned_data['title']
                try:
                    validate_dashes(isbnType, isbnId)
                    validate_isbn_len(isbnType, isbnId)
                except ValueError as exception:
                    return isbn_validation_error(request, template, form)
                else:
                    book = form.save(commit=False)
                    book.isbnId = isbnId.replace("-", "")
                    book.save()
                    return render(request, template, {'title': title,
                                                      'form': form})
            except Exception as exception:
                return generic_error(request, exception)
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
        return generic_error(request, exception)


def book_edit(request, pk):
    try:
        template = 'book_edit.html'
        book = get_object_or_404(Book, pk=pk)
        if request.method == "POST":
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                isbnType = form.cleaned_data['isbnType']
                isbnId = form.cleaned_data['isbnId']
                title = form.cleaned_data['title']
                try:
                    validate_dashes(isbnType, isbnId)
                    validate_isbn_len(isbnType, isbnId)
                except ValueError:
                    return isbn_validation_error(request, template, form)
                else:
                    book = form.save(commit=False)
                    book.isbnId = isbnId.replace("-", "")
                    book.save()
                    return render(request, template, {'title': title,
                                                      'form': form})
        else:
            form = BookForm(instance=book)
        return render(request, template, {'form': form})
    except Exception as exception:
        return generic_error(request, exception)


def book_search(request):
    try:
        template = 'book_search.html'
        keyword = word = request.GET.get('keyword')
        parameter = request.GET.get('parameter')

        if (parameter == 'publishedDate'):
            try:
                word = word.split()
                if len(word) == 3:
                    word.remove('to')
                    dateStart = datetime.date.fromisoformat(word[0])
                    dateEnd = datetime.date.fromisoformat(word[1])
                    word.clear()
                    word.extend([str(dateStart), str(dateEnd)])
                    searchword = parameter + "__range"
                elif len(word) == 1:
                    word = datetime.date.fromisoformat(word[0])
                    searchword = parameter + "__icontains"
                else:
                    raise ValueError
            except ValueError:
                return date_error(request, template)
        else:
            searchword = parameter + "__icontains"
        book_list = Book.objects.filter(
            Q(**{searchword: word})
        )
        page = request.GET.get('page', 1)
        pageSize = 5
        books = paginator(book_list, page, pageSize)
        return render(request, template, {'books': books,
                                          'keyword': keyword,
                                          'parameter': parameter})
    except Exception as exception:
        response = generic_error(request, exception)
        return response


def book_advanced_searching(request):
    template = 'book_advanced_searching.html'
    if request.method == 'GET':
        if (len(request.GET) > 0):
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
            book_list = Book.objects.filter(advanced_filter)
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
                                                   'title': searchdict["title"],
                                                   'authors': searchdict["authors"],
                                                   'language': searchdict["language"],
                                                   'isbnId': searchdict["isbnId"],
                                                   'pageCount': searchdict["pageCount"],
                                                   'dateStart':dateStart,
                                                   'dateEnd': dateEnd, 
                                                   'exactDate': searchdict["publishedDate"]})
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
