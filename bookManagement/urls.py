from django.urls import path

from . import views

appname = 'bookManagement'
urlpatterns = [
    path('', views.index, name='index'),
    path('book_add', views.book_add, name='book_add'),
    path('book_list', views.book_list, name='book_list'),
    path('book_remove_<int:pk>', views.book_remove, name='book_remove'),
    path('book_search', views.book_search, name='book_search'),
    path('book_edit_<int:pk>', views.book_edit, name='book_edit'),
    path('book_advanced_searching', views.book_advanced_searching,
         name='book_advanced_searching'),
    path('feed_from_google', views.feed_from_google,
         name='feed_from_google'),
    path('api/books/', views.BookList.as_view(), name='book_api'),
    ]
