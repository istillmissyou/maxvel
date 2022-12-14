from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, BooleanField, CharField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField)


class Category(Model):
    name = CharField(max_length=50, unique=True)


class Ingredient(Model):
    name = CharField(max_length=50)
    measurement_unit = CharField(max_length=30)
    amount = PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
        )
    )


class ImagePositions(Model):
    image = ImageField(upload_to='position', blank=True, null=True)


class Position(Model):
    name = CharField(max_length=50)
    price = PositiveSmallIntegerField()
    new = BooleanField(default=False)
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
    images = ManyToManyField(
        ImagePositions,
        related_name='positions',
    )
    text = TextField()
