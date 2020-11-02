from django.urls import path

from . import views

appname = 'bookManagement'
urlpatterns = [
    path('', views.index, name='index'),
    path('book_add', views.book_add, name='book_add')
]