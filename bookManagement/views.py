from django.http import HttpResponse
from django.http import request
from django.shortcuts import render, redirect

from .forms import BookForm


def index(request):
    return render(request, 'index.html')

def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('bookManagement:book_add')
            except Exception as exception:
                error = "Something went wrong. If error occurs often please send error message contained below to administator."
                error_message = str(exception)
                return render(request, 'error.html', {'em':error_message, 'e':error})
    else:
        form = BookForm()
    return render(request, 'book_add.html', {'form':form})            
