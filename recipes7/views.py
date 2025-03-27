# recipes/views.py
from django.shortcuts import render
 
def vege_view(request):
    return render(request, 'recipes7/vege.html')
