# recipes/urls.py
from django.urls import path
from . import views
 
app_name = 'recipes9'
 
urlpatterns = [
    path('new/', views.new_view, name='new'),
]