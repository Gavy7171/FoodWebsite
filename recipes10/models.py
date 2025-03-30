# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg, Count

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE, 
                                 related_name='subcategories', 
                                 null=True, 
                                 blank=True)
    
    def __str__(self):
        return f"{self.name} {f'({self.category.name})' if self.category else ''}"
    
    class Meta:
        verbose_name_plural = "Subcategories"
        ordering = ['name']
        unique_together = ['name', 'category']

class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Cuisines"
        ordering = ['name']

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]
    
    # Basic Recipe Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    
    # Optional Relationships
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        related_name='recipes', 
        null=True, 
        blank=True
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.SET_NULL, 
        related_name='recipes', 
        null=True, 
        blank=True
    )
    cuisine = models.ForeignKey(
        Cuisine, 
        on_delete=models.SET_NULL, 
        related_name='recipes', 
        null=True, 
        blank=True
    )
    
    # Author and Ownership
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='recipes'
    )
    
    # Diet and Lifestyle Tags
    vegetarian = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)
    keto = models.BooleanField(default=False)
    
    # Additional Fields
    image = models.ImageField(
        upload_to='recipe_images/', 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    
    # Favorites
    favorites = models.ManyToManyField(
        User, 
        related_name='favorite_recipes', 
        blank=True
    )
    
    def __str__(self):
        return self.title
    
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time
    
    @property
    def avg_rating(self):
        """Calculate average rating from all reviews"""
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg) if avg else 0
    
    @property
    def total_ratings(self):
        """Count total number of reviews/ratings"""
        return self.reviews.count()
    
    class Meta:
        ordering = ['-created_at']
        get_latest_by = 'created_at'

class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='ingredients'
    )
    quantity = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.quantity} {self.name}"
    
    class Meta:
        ordering = ['id']

class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='steps'
    )
    order = models.PositiveIntegerField()
    description = models.TextField()
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Step {self.order} for {self.recipe.title}"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['recipe', 'user']  # One review per user per recipe
        
    def __str__(self):
        return f"{self.user.username}'s {self.rating}-star review of {self.recipe.title}"