from .models import Category, Ingredient, IngredientsInPosition, Position
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField)
from django.db.models import F
from rest_framework import serializers

<<<<<<< HEAD

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
=======
from .models import IngredientsInPosition, Position


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.Base64ImageField()
>>>>>>> refs/remotes/origin/backend

    class Meta:
        fields = '__all__'
        model = Position

<<<<<<< HEAD
    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredient_position__amount'),
        )
        return ingredients

=======
>>>>>>> refs/remotes/origin/backend
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
