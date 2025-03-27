# recipes/views.py
from django.shortcuts import render
 
def breakfast_view(request):
    return render(request, 'recipes1/breakfast.html')