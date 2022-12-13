from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import IngredientsInPosition, Position


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.Base64ImageField()

    class Meta:
        fields = '__all__'
        model = Position

    @staticmethod
    def create_ingredients(ingredients, position, amount_ingredients):
        for ingredient in ingredients:
            IngredientsInPosition.objects.create(
                position=position, ingredient=ingredient,
                amount=amount_ingredients
            )

    def create(self, validated_data):
        # author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        amount_ingredients = validated_data.pop('amount_ingredients')
        categories = validated_data.pop('category')
        position = Position.objects.create(**validated_data)
        for category in categories:
            position.category.add(category)
        for ingredient in ingredients:
            position.ingredients.add(ingredient)
        self.create_ingredients(ingredients, position, amount_ingredients)
        return position

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientsInPosition.objects.filter(position=instance).delete()
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)