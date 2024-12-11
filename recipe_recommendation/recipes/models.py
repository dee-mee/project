from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)

class ingredient(models.Model):
    name = models.CharField(max_length=100)

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(ingredient)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    instructions = models.TextField()
    prep_time = models.IntegerField()               #in minutes

class UserTry(models.Model):
    user_email = models.EmailField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)