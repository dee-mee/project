from .models import Recipe

def add_recipes_to_context(request):
    """Add all recipes to the context globally."""
    return {'recipes': Recipe.objects.all()}
