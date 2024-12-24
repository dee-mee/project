from django.contrib import admin

# Register your models here.
from .models import Recipe, Ingredient, Location

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Customize the Recipe admin interface."""
    list_display = ('title', 'prep_time', 'location')  # Fields displayed in the list view
    list_filter = ('location', 'prep_time')  # Filters on the right side
    search_fields = ('title', 'ingredients__name')  # Searchable fields

    # Display ingredients as a comma-separated list in the admin interface
    def get_ingredients(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])
    get_ingredients.short_description = 'Ingredients'



@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Customize the Ingredient admin interface."""
    list_display = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Customize the Location admin interface."""
    list_display = ('name',)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1




