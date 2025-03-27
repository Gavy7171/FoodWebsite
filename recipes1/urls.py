# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes1'
 
urlpatterns = [
    path('breakfast/', views.breakfast_view, name='breakfast'),
]
 