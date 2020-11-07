"""TODO:
    - Unit tests
"""

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
        book_list = BookOperations.simple_search(request)
        page = request.GET.get('page', 1)
        pageSize = 5
        books = paginator(book_list, page, pageSize)
        return render(request, template, {
            'books': books,
            'keyword': request.GET.get('keyword'),
            'dateExact': request.GET.get('dateExact'),
            'dateFrom': request.GET.get('dateFrom'),
            'dateTo': request.GET.get('dateTo'),
            'parameter': request.GET.get('parameter'),
            })
    except Exception as exception:
        return ErrorHandler.generic_error(request, exception)


def book_advanced_searching(request):
    template = 'book_advanced_searching.html'
    if request.method == 'GET':
        if len(request.GET) > 0:
            book_list = BookOperations.advanced_search(request)
            page = request.GET.get('page', 1)
            pageSize = 5
            books = paginator(book_list, page, pageSize)
            if not book_list.exists():
                nobooks = True
                return render(request, template, {'nobooks': nobooks,
                              'books': books})
            else:
                return render(request, template, {
                    'books': books,
                    'parameter': request.GET.get('parameter'),
                    'dateParam': request.GET.get('dateParameter'),
                    'title': request.GET.get('title'),
                    'authors': request.GET.get('authors'),
                    'language': request.GET.get('language'),
                    'isbnId': request.GET.get('isbnId'),
                    'pageCount': request.GET.get('pageCount'),
                    'dateStart': request.GET.get('dateStart'),
                    'dateEnd': request.GET.get('dateEnd'),
                    'exactDate': request.GET.get('exactDate'),
                    })
        else:
            return render(request, template)
    else:
        return render(request, template)


def feed_from_google(request):
    template = 'feed_from_google.html'
    resultNumbers = request.GET.get("resultNumbers")
    if request.method == 'GET' and resultNumbers:
        returnData = BookOperations.import_from_google_api(request)
        return render(request, template, {'addedCounter': returnData[0],
                                          'noItems': returnData[1]})
    else:
        return render(request, template)
