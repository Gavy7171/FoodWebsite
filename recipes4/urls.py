# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes4'
 
urlpatterns = [
    path('dessert/', views.dessert_view, name='dessert'),
]