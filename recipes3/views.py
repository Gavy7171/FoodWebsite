# recipes/views.py
from django.shortcuts import render
 
def dinner_view(request):
    return render(request, 'recipes3/dinner.html')