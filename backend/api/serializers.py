from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField)

from .models import Category, ImagePositions, Ingredient, Position


class IngredientSerializer(ModelSerializer):
    amount = IntegerField()

    class Meta:
        model = Ingredient
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ImagePositionsSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ImagePositions
        fields = ('image',)


class PositionViewSerializer(ModelSerializer):
    ingredients = serializers.SerializerMethodField(
        read_only=True,
        source='get_ingredients',
    )
    images = serializers.SerializerMethodField(
        read_only=True,
        source='get_images',
    )

    class Meta:
        model = Position
        fields = '__all__'

    def get_ingredients(self, obj):
        return IngredientSerializer(
            Ingredient.objects.filter(positions=obj),
            many=True,
        ).data

    def get_images(self, obj):
        return ImagePositionsSerializer(
            ImagePositions.objects.filter(positions=obj),
            many=True,
        ).data


class PositionCreateSerializer(ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    images = ImagePositionsSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Position

    @staticmethod
    def create_ingredients(ingredients, position):
        for ingredient in ingredients:
            new_ingredient = Ingredient.objects.create(
                name=ingredient['name'],
                measurement_unit=ingredient['measurement_unit'],
                amount=ingredient['amount']
            )
            position.ingredients.add(new_ingredient)

    @staticmethod
    def create_image(images, position):
        for image in images:
            new_image = ImagePositions.objects.create(
                image=image['image']
            )
            position.images.add(new_image)

    def create(self, validated_data):
        # author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients', None)
        images = validated_data.pop('images', None)
        categories = validated_data.pop('category', None)
        position = Position.objects.create(**validated_data)
        position.category.set(categories)
        self.create_ingredients(ingredients, position)
        self.create_image(images, position)
        return position

    def update(self, instance, validated_data):
        Ingredient.objects.filter(positions=instance).delete()
        images_positions = ImagePositions.objects.filter(positions=instance)
        for image in images_positions:
            image.image.delete(save=True)
            image.delete()
        ingredients = validated_data.pop('ingredients', None)
        images = validated_data.pop('images', None)
        self.create_ingredients(ingredients, instance)
        self.create_image(images, instance)
        return super().update(instance, validated_data)
