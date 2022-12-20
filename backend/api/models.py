import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              EmailField, ForeignKey, ImageField, IntegerField,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField)
from django.utils.translation import gettext_lazy as _


class Category(Model):
    name = CharField(max_length=50, unique=True)
    order = IntegerField(default=0)

    class Meta:
        ordering = ('-order',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# class Ingredient(Model):
#     name = CharField(max_length=50)
#     measurement_unit = CharField(max_length=30)
#     amount = PositiveSmallIntegerField(
#         validators=(
#             MinValueValidator(1),
#         )
#     )

#     class Meta:
#         verbose_name = 'Ингридиент'
#         verbose_name_plural = 'Ингридиенты'

#     def __str__(self):
#         return self.name


class Position(Model):
    name = CharField(max_length=50)
    price = PositiveSmallIntegerField()
    new = BooleanField(default=False)
    amount = PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
        )
    )
    text = TextField()
    # ingredients = ManyToManyField(
    #     Ingredient,
    #     related_name='positions',
    # )
    ingredients = CharField(max_length=50)
    category = ManyToManyField(
        Category,
        related_name='positions',
    )
    image = ImageField(upload_to='position', blank=True, null=True)

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return self.name

    def remove_on_image_update(self):
        try:
            obj = Position.objects.get(id=self.id)
        except Position.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        # for ingredient in self.ingredients.all():
        #     ingredient.delete()
        self.image.delete()
        return super(Position, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(Position, self).save(*args, **kwargs)


class PosithionForShopingCart(Model):
    position = ForeignKey(Position, on_delete=CASCADE)
    amount = PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
        )
    )


class ShoppingCart(Model):
    positions_in_cart = ManyToManyField(PosithionForShopingCart)
    all_amount = IntegerField()
    name_user = CharField(max_length=100)
    phone = CharField(max_length=12)
    email = EmailField(max_length=255)
    address = CharField(max_length=1024)
    date_start = DateTimeField()
    comment = CharField(max_length=1024)
    pub_date = DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def validate(self):
        new_number = phonenumbers.parse(self.phone, "RU")
        if phonenumbers.is_valid_number(new_number) is False:
            raise ValidationError(_('Поле телефона не корректное'))
        # if len(self.phone) != 11:
        #     raise ValidationError(_('Поле телефона должно состоять из 11 цифр'))
