# recipes/views.py
from django.shortcuts import render
 
def dessert_view(request):
    return render(request, 'recipes4/dessert.html')