# forms.py
from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Recipe, Ingredient, Step, Category, Subcategory, Cuisine

class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure category field
        self.fields['category'].required = False
        self.fields['category'].empty_label = "Select a category (optional)"
        
        # Configure subcategory field
        self.fields['subcategory'].required = False
        self.fields['subcategory'].empty_label = "Select a subcategory (optional)"
        
        # Configure cuisine field
        self.fields['cuisine'].required = False
        self.fields['cuisine'].empty_label = "Select cuisine (optional)"
        
        # Dynamically filter subcategories based on selected category
        if self.data.get('category'):
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields['subcategory'].queryset = Subcategory.objects.none()
        elif self.instance.pk and self.instance.category:
            # For existing recipes, filter subcategories by the recipe's category
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            # Show all subcategories if no category is selected
            self.fields['subcategory'].queryset = Subcategory.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that if a subcategory is selected, its category matches the selected category
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        
        if category and subcategory and subcategory.category != category:
            # Clear subcategory if it doesn't match the selected category
            cleaned_data['subcategory'] = None
        
        return cleaned_data

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'prep_time', 'cook_time', 'servings',
            'difficulty', 'category', 'subcategory', 'cuisine', 
            'vegetarian', 'vegan', 'gluten_free', 'keto', 
            'image', 'notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Recipe Title', 
                'required': 'required'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Brief description of your recipe', 
                'required': 'required'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Prep time in minutes', 
                'required': 'required',
                'min': '0'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Cooking time in minutes', 
                'required': 'required',
                'min': '0'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Number of servings', 
                'required': 'required',
                'min': '1'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control', 
                'required': 'required'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subcategory': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cuisine': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Additional notes, tips, or variations'
            }),
            'vegetarian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vegan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gluten_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'keto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category if category else None

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['quantity', 'name']
        widgets = {
            'quantity': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Amount'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingredient name',
                'required': 'required'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise ValidationError("Ingredient name cannot be empty.")
        return name

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Step instructions',
                'rows': 3,
                'required': 'required'
            }),
        }
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise ValidationError("Step description cannot be empty.")
        return description

# Create formsets for ingredients and steps
IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, 
    form=IngredientForm, 
    extra=1, 
    can_delete=False,
    min_num=1,
    validate_min=True
)

StepFormSet = inlineformset_factory(
    Recipe, Step, 
    form=StepForm, 
    extra=1, 
    can_delete=False,
    min_num=1,
    validate_min=True
)