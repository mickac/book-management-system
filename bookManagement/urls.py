from django.urls import path

from . import views

appname = 'bookManagement'
urlpatterns = [
    path('', views.index, name='index'),
]