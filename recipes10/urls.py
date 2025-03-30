from django.urls import path
from . import views

app_name = 'recipes10'

urlpatterns = [
    # Recipe browsing
    path('', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('category/<slug:category_slug>/', views.category_recipes, name='category_recipes'),
    
    # Recipe management
    path('recipes/submit/', views.submit_recipe, name='submit_recipe'),
    path('recipes/my/', views.my_recipes, name='my_recipes'),
    path('recipes/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipes/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    
    # Favorites
    path('recipes/<int:recipe_id>/favorite/', views.favorite_recipe, name='favorite_recipe'),
    path('recipes/favorites/', views.favorite_recipes, name='favorite_recipes'),
    
    # Utility
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
]