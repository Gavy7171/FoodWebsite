# recipes/views.py
from django.shortcuts import render
 
def new_view(request):
    return render(request, 'recipes9/new.html')
