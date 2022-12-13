from django.db.models import F
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Ingredient, IngredientsInPosition, Position


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = Ingredient
        read_only_fields = ['id', 'name', 'measurement_unit']

        def get_amount(self, obj):
            return obj.ingredientinrecipe.values('amount')[0].get('amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    # image = Base64ImageField()

    class Meta:
        fields = '__all__'
        model = Position

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredient_in_recipe__amount'),
        )
        return ingredients
    
    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            get_ingredient = Ingredient.objects.get(id=ingredient['id'])
            IngredientsInPosition.objects.create(
                recipe=recipe, ingredient=get_ingredient,
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        # author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        categories = validated_data.pop('category')
        recipe = Position.objects.create(**validated_data)
        for category in categories:
            recipe.category.add(category)
        for ingredient in ingredients:
            recipe.ingredients.add(ingredient)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientsInPosition.objects.filter(recipe=instance).delete()
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)