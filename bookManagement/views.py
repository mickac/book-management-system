from django.http import HttpResponse


def index(request):
    return HttpResponse("Testing bookManagement on Heroku")