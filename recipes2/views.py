# recipes/views.py
from django.shortcuts import render
 
def lunch_view(request):
    return render(request, 'recipes2/lunch.html')
