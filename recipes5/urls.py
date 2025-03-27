# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes5'
 
urlpatterns = [
    path('drinks/', views.drinks_view, name='drinks'),
]