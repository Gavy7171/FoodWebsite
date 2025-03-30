# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Recipe, Category, Subcategory, Cuisine, Ingredient, Step
from .forms import RecipeForm, IngredientFormSet, StepFormSet

def get_subcategories(request):
    """
    AJAX view to get subcategories for a given category
    """
    category_id = request.GET.get('category_id')
    try:
        subcategories = list(Subcategory.objects.filter(category_id=category_id).values('id', 'name'))
        return JsonResponse(subcategories, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def submit_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        step_formset = StepFormSet(request.POST, prefix='steps')
        
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            # Save recipe
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            
            # Save ingredients
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                if ingredient.name.strip():
                    ingredient.recipe = recipe
                    ingredient.save()
            
            # Save steps and ensure they're in order
            steps = step_formset.save(commit=False)
            for i, step in enumerate(steps):
                if step.description.strip():
                    step.recipe = recipe
                    step.order = i + 1
                    step.save()
            
            messages.success(request, "Your recipe has been submitted successfully!")
            return redirect('recipes10:recipe_detail', recipe.id)
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        step_formset = StepFormSet(prefix='steps')

    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'all_categories': Category.objects.all(),
        'all_subcategories': Subcategory.objects.all(),
        'all_cuisines': Cuisine.objects.all(),
    }
    return render(request, 'recipes10/submit_recipe.html', context)

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(ingredients__name__icontains=query)
        ).distinct()
    
    # Filter by category if requested
    category_id = request.GET.get('category')
    if category_id:
        recipes = recipes.filter(category_id=category_id)
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'query': query or '',
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'recipes10/recipe_list.html', context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Get similar recipes (same category, excluding this one)
    similar_recipes = Recipe.objects.filter(category=recipe.category).exclude(id=recipe_id)[:3]
    
    context = {
        'recipe': recipe,
        'similar_recipes': similar_recipes,
        'categories': Category.objects.all(),
    }
    return render(request, 'recipes10/recipe_detail.html', context)

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'recipes': recipes,
        'categories': Category.objects.all(),
    }
    return render(request, 'recipes10/my_recipes.html', context)

def category_recipes(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    recipes = Recipe.objects.filter(category=category).order_by('-created_at')
    
    context = {
        'category': category,
        'recipes': recipes,
        'categories': Category.objects.all(),
    }
    return render(request, 'recipes10/category_recipes.html', context)

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(request.POST, instance=recipe, prefix='steps')
        
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            # Save recipe
            recipe = form.save()
            
            # Handle ingredients
            ingredient_formset.save()
            
            # Handle steps
            steps = step_formset.save(commit=False)
            for i, step in enumerate(steps):
                step.recipe = recipe
                step.order = i + 1
                step.save()
            
            messages.success(request, "Your recipe has been updated successfully!")
            return redirect('recipes10:recipe_detail', recipe.id)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(instance=recipe, prefix='steps')
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'recipe': recipe,
        'all_categories': Category.objects.all(),
        'all_subcategories': Subcategory.objects.filter(category=recipe.category),
        'all_cuisines': Cuisine.objects.all(),
    }
    return render(request, 'recipes10/edit_recipe.html', context)

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "Your recipe has been deleted successfully!")
        return redirect('recipes10:my_recipes')
    
    context = {
        'recipe': recipe,
        'categories': Category.objects.all(),
    }
    return render(request, 'recipes10/delete_recipe.html', context)

@login_required
def favorite_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == 'POST':
        if recipe.favorites.filter(id=request.user.id).exists():
            recipe.favorites.remove(request.user)
            messages.success(request, "Recipe removed from favorites.")
        else:
            recipe.favorites.add(request.user)
            messages.success(request, "Recipe added to favorites.")
        
        return redirect('recipes10:recipe_detail', recipe_id)
    
    return redirect('recipes10:recipe_list')

def favorite_recipes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    recipes = Recipe.objects.filter(favorites=request.user).order_by('-created_at')
    
    context = {
        'recipes': recipes,
        'categories': Category.objects.all(),
    }
    return render(request, 'recipes10/favorite_recipes.html', context)