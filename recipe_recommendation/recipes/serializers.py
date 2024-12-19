from rest_framework import serializers

from .models import Recipe, UserTry

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe model."""
    class Meta:
        model = Recipe
        fields = '__all__'

class UserTrySerializer(serializers.ModelSerializer):
    """Serializer for the UserTry model."""
    class Meta:
        model = UserTry
        fields = '__all__'
