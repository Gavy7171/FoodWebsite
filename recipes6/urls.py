# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes6'
 
urlpatterns = [
    path('keto/', views.keto_view, name='keto'),
]