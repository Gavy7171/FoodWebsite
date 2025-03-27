# recipes/views.py
from django.shortcuts import render
 
def drinks_view(request):
    return render(request, 'recipes5/drinks.html')