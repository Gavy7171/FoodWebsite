# recipes/views.py
from django.shortcuts import render
 
def keto_view(request):
    return render(request, 'recipes6/keto.html')
