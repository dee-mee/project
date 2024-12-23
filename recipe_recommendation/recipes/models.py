from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    prep_time = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient)  # Ensure this is defined

    def __str__(self):
        return self.title



class UserTry(models.Model):
    """Model to track user attempts on recipes."""
    user_email = models.EmailField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.recipe.title}"



class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()  # Description of the action
    timestamp = models.DateTimeField(auto_now_add=True)  # When it happened

    def __str__(self):
        return f"{self.user.username} - {self.action}"