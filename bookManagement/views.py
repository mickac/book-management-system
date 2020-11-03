"""
    TODO:
    - ISBN Validation (if ISBN-13 have 17 characters with dashes is good, but user can enter 17 characters without dashes - system will accept that, but value is wrong)
    - Fixing pagination with search functionality

"""


from django.http import HttpResponse
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import(
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.db.models import Q

from .forms import BookForm
from .models import Book

import datetime

def index(request):
    return render(request, 'index.html')

def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                isbnType = form.cleaned_data['isbnType']
                isbnId = form.cleaned_data['isbnId']
                bookTitle = form.cleaned_data['title']
                dashCounter = isbnId.count("-")
                isbnId = isbnId.replace("-","")

                if(isbnType == 'ISBN-10' and len(isbnId) != 10):
                    error = "You have to enter ISBN ID of length 10 (or 13 with '-' chars) for ISBN Type 10."
                    return render(request, 'book_add.html', {'e':error, 'form':form})
                elif(isbnType == 'ISBN-13' and len(isbnId) != 13):
                    error = "You have to enter ISBN ID of length 13 (or 17 with '-' chars) for ISBN Type 13."
                    return render(request, 'book_add.html', {'e':error, 'form':form})
                else:
                    form.save()
                    form = BookForm()
                    return render(request, 'book_add.html', {'title':bookTitle, 'form':form})
            except Exception as exception:
                error = "Something went wrong. If error occurs often please send error message contained below to administator."
                error_message = str(exception)
                return render(request, 'error.html', {'em':error_message, 'e':error})
    else:
        form = BookForm()
    return render(request, 'book_add.html', {'form':form})            

def book_list(request):
    try:
        book_list = Book.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(book_list, 5)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        return render(request, 'book_list.html', { 'books': books })
    except Exception as exception:
        error = "Something went wrong. If error occurs often please send error message contained below to administator."
        error_message = str(exception)
        return render(request, 'error.html', {'em':error_message, 'e':error})

def book_search(request):
        try:
            keyword = request.POST.get('keyword')
            parameter = request.POST.get('parameter')
            if (parameter == 'title'):
                book_list = Book.objects.filter(
                    Q(title__icontains=keyword)
                )
            elif (parameter == 'authors'):
                book_list = Book.objects.filter(
                    Q(authors__icontains=keyword)
                )
            elif (parameter == 'language'):
                book_list = Book.objects.filter(
                    Q(language__icontains=keyword)
                )
            elif (parameter == 'publishedDate'):
                format = "%Y-%m-%d"
                try:
                    keyword = keyword.split()
                    if (len(keyword) == 3):
                        keyword.remove('to')
                        dateStart = datetime.datetime.strptime(keyword[0], format)
                        dateEnd = datetime.datetime.strptime(keyword[1], format)
                        book_list = Book.objects.filter(
                            Q(publishedDate__range=[dateStart, dateEnd])
                        )
                    elif(len(keyword) == 1):
                        date = datetime.datetime.strptime(keyword[0], format)
                        book_list = Book.objects.filter(
                            Q(publishedDate__icontains=date)
                        )
                    else:
                        raise ValueError
                except ValueError:
                    error = "There is something wrong with date range you have passed. For additional information about search functionality, click question mark near search field. If error still occures contact the administrator."
                    return render(request, 'book_search.html', { 'error':error })
            else:
                error = "Please choose parameter first!"
                return render(request, 'book_search.html', { 'error':error })
            
            page = request.GET.get('page', 1)
            paginator = Paginator(book_list, 5)

            try:
                books = paginator.page(page)
            except PageNotAnInteger:
                books = paginator.page(1)
            except EmptyPage:
                books = paginator.page(paginator.num_pages)

            return render(request, 'book_search.html', { 'books': books }) 
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})

def book_edit(request, pk):
    try:
        book = get_object_or_404(Book, pk=pk)
        if request.method == "POST":
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                isbnType = form.cleaned_data['isbnType']
                isbnId = form.cleaned_data['isbnId']
                bookTitle = form.cleaned_data['title']
                isbnId = isbnId.replace("-","")
                if(isbnType == 'ISBN-10' and len(isbnId) != 10):
                    error = "You have to enter ISBN ID of length 10 (or 13 with '-' chars) for ISBN Type 10."
                    return render(request, 'book_edit.html', {'e':error, 'form':form})
                elif(isbnType == 'ISBN-13' and len(isbnId) != 13):
                    error = "You have to enter ISBN ID of length 13 (or 17 with '-' chars) for ISBN Type 13."
                    return render(request, 'book_edit.html', {'e':error, 'form':form})
                else:
                    form.save()
                    return render(request, 'book_edit.html', {'title':bookTitle, 'form':form})
        else:
            form = BookForm(instance=book)
        return render(request, 'book_edit.html', {'form':form}) 
    except Exception as exception:
        error = "Something went wrong. If error occurs often please send error message contained below to administator."
        error_message = str(exception)
        return render(request, 'error.html', {'em':error_message, 'e':error})