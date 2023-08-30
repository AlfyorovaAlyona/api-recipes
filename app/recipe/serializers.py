"""Serializers for Resipe API."""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer."""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_min', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Detailed recipe (recipe+description) serializer."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
