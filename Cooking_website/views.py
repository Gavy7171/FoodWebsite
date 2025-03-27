from django.shortcuts import render
from django.http import HttpResponse

def Recepies(request):
    # return HttpResponse(request, "Hello world!")
    return render(request, 'home.html')

    