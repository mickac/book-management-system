"""
    TODO:
    - PEP8 Validation + Doing some modules for repeating methods
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
                #[1],[6],[11] - ISBN-10
                #[3],[5],[10],[15] -ISBN-13
                try:
                    dashesValidation = True
                    dashesValidationString = list(isbnId)
                    dashCounter = dashesValidationString.count('-')
                    if(isbnType == 'ISBN-10' and ((dashesValidationString[1] != '-' or dashesValidationString[6] != '-' or dashesValidationString[11] != '-') and dashCounter == 3)):
                        dashesValidation = False
                    if(isbnType == 'ISBN-13' and ((dashesValidationString[3] != '-' or dashesValidationString[5] != '-' or dashesValidationString[10] != '-' or dashesValidationString[15] != '-') and dashCounter == 4)):
                        dashesValidation = False
                    isbnId = isbnId.replace("-","")
                except:
                    error = "Wrong ISBN ID!"
                    return render(request, 'book_add.html', {'e':error, 'form':form})

                if(isbnType == 'ISBN-10' and (len(isbnId) != 10 or dashesValidation == False)):
                    error = "Wrong ISBN ID for ISBN-10 type. Check ISBN ID and try again! (Length should be 10 without dashes or 13 with dashes)"
                    return render(request, 'book_add.html', {'e':error, 'form':form})
                elif(isbnType == 'ISBN-13' and len(isbnId) != 13 and dashesValidation == False):
                    error = "Wrong ISBN ID for ISBN-13 type. Check ISBN ID and try again! (Length should be 13 without dashes or 17 with dashes)"
                    return render(request, 'book_add.html', {'e':error, 'form':form})
                else:
                    book = form.save(commit=False)
                    book.isbnId = isbnId
                    book.save()
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
            keyword = request.GET.get('keyword')
            parameter = request.GET.get('parameter')
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

            return render(request, 'book_search.html', { 'books': books, 'keyword':keyword, 'parameter':parameter }) 
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
                try:
                    dashesValidation = True
                    dashesValidationString = list(isbnId)
                    dashCounter = dashesValidationString.count('-')
                    if(isbnType == 'ISBN-10' and ((dashesValidationString[1] != '-' or dashesValidationString[6] != '-' or dashesValidationString[11] != '-') and dashCounter == 3)):
                        dashesValidation = False
                    if(isbnType == 'ISBN-13' and ((dashesValidationString[3] != '-' or dashesValidationString[5] != '-' or dashesValidationString[10] != '-' or dashesValidationString[15] != '-') and dashCounter == 4)):
                        dashesValidation = False
                    isbnId = isbnId.replace("-","")
                except:
                    error = "Wrong ISBN ID!"
                    return render(request, 'book_edit.html', {'e':error, 'form':form})

                if(isbnType == 'ISBN-10' and (len(isbnId) != 10 or dashesValidation == False)):
                    error = "Wrong ISBN ID for ISBN-10 type. Check ISBN ID and try again! (Length should be 10 without dashes or 13 with dashes)"
                    return render(request, 'book_edit.html', {'e':error, 'form':form})
                elif(isbnType == 'ISBN-13' and len(isbnId) != 13 and dashesValidation == False):
                    error = "Wrong ISBN ID for ISBN-13 type. Check ISBN ID and try again! (Length should be 13 without dashes or 17 with dashes)"
                    return render(request, 'book_edit.html', {'e':error, 'form':form})
                else:
                    book = form.save(commit=False)
                    book.isbnId = isbnId
                    book.save()
                    return render(request, 'book_edit.html', {'title':bookTitle, 'form':form})
        else:
            form = BookForm(instance=book)
        return render(request, 'book_edit.html', {'form':form}) 
    except Exception as exception:
        error = "Something went wrong. If error occurs often please send error message contained below to administator."
        error_message = str(exception)
        return render(request, 'error.html', {'em':error_message, 'e':error})