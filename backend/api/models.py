from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField)


class Category(Model):
    name = CharField(max_length=50)


class Ingredient(Model):
    name = CharField(max_length=50)
    measurement_unit = CharField(max_length=30)


class Position(Model):
    name = CharField(max_length=50)
    image = ImageField(upload_to='positions')
    price = PositiveSmallIntegerField()
    category = ManyToManyField(
        Category,
        related_name='positions',
    )
    amount = PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
        )
    )
    ingredients = ManyToManyField(
        Ingredient,
        related_name='positions',
    )
    text = TextField()


class IngredientsInPosition(Model):
    position = ForeignKey(
        Position,
        on_delete=CASCADE,
        related_name='ingredient_position',
    )
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name='ingredient_position',
    )
    amount = PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
        )
    )
