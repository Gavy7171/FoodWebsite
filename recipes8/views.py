# recipes/views.py
from django.shortcuts import render
 
def mother_view(request):
    return render(request, 'recipes8/mother.html')
