from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField)

from .models import Category, Ingredient, IngredientsInPosition, Position


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit',
    )
    amount = IntegerField()

    class Meta:
        model = IngredientsInPosition
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = '__all__'
        model = Position

    # def get_ingredients(self, obj):
    #     ingredients = obj.ingredients.values(
    #         'id',
    #         'name',
    #         'measurement_unit',
    #         amount=F('ingredient_position__amount'),
    #     )
    #     return ingredients

    # @staticmethod
    # def create_ingredients(ingredients, position, amount_ingredients):
    #     for ingredient in ingredients:
    #         IngredientsInPosition.objects.create(
    #             position=position, ingredient=ingredient,
    #             amount=amount_ingredients
    #         )

    # def create(self, validated_data):
    #     # author = self.context.get('request').user
    #     ingredients = validated_data.pop('ingredients')
    #     # amount_ingredients = validated_data.pop('amount_ingredients')
    #     categories = validated_data.pop('category')
    #     position = Position.objects.create(**validated_data)
    #     for category in categories:
    #         position.category.add(category)
    #     for ingredient in ingredients:
    #         position.ingredients.add(ingredient)
    #     self.create_ingredients(ingredients, position, amount_ingredients)
    #     return position

    # def update(self, instance, validated_data):
    #     instance.tags.clear()
    #     IngredientsInPosition.objects.filter(position=instance).delete()
    #     self.create_ingredients(validated_data.pop('ingredients'), instance)
    #     return super().update(instance, validated_data)
