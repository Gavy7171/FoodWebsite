# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes8'
 
urlpatterns = [
    path('mother/', views.mother_view, name='mother'),
]