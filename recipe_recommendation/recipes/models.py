from django.db import models

class Location(models.Model):
    """Model to store user locations."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Model to store individual ingredients."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.ManyToManyField('Ingredient')
    instructions = models.TextField()
    prep_time = models.IntegerField()
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)  # Add this field

    def __str__(self):
        return self.title


class UserTry(models.Model):
    """Model to track user attempts on recipes."""
    user_email = models.EmailField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.recipe.title}"
