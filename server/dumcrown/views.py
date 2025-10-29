from django.http import HttpResponse


def teste(request):
    return HttpResponse("ola mundo")
