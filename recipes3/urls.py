# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes3'
 
urlpatterns = [
    path('dinner/', views.dinner_view, name='dinner'),
]