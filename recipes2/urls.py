# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes2'
 
urlpatterns = [
    path('lunch/', views.lunch_view, name='lunch'),
]
 