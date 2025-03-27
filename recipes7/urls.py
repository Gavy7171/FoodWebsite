# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes7'
 
urlpatterns = [
    path('vege/', views.vege_view, name='vege'),
]