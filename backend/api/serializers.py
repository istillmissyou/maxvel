from .models import Category, Ingredient, IngredientsInPosition, Position
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField)
from django.db.models import F
from rest_framework import serializers


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


class RecipeSerializer(ModelSerializer):
    # ingredients = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField('amount')
    # image = Base64ImageField()

    class Meta:
        fields = '__all__'
        model = Position

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredient_position__amount'),
        )
        return ingredients

    @staticmethod
    def create_ingredients(ingredients, recipe, amount):
        for ingredient in ingredients:
            get_ingredient = Ingredient.objects.get(id=ingredient)
            IngredientsInPosition.objects.create(
                recipe=recipe, ingredient=get_ingredient,
                amount=amount
            )

    def create(self, validated_data):
        # author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        amount = validated_data.pop('amount')
        categories = validated_data.pop('category')
        recipe = Position.objects.create(**validated_data)
        for category in categories:
            recipe.category.add(category)
        for ingredient in ingredients:
            recipe.ingredients.add(ingredient)
        self.create_ingredients(ingredients, recipe, amount)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientsInPosition.objects.filter(recipe=instance).delete()
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)
