import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              EmailField, ForeignKey, ImageField, IntegerField,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField)
from django.utils.translation import gettext_lazy as _


class Category(Model):
    name = CharField(
        verbose_name='Наименование',
        max_length=50,
        unique=True,
    )
    order = IntegerField(
        verbose_name='Очередность отображения',
        help_text='По возвростанию',
        default=0
    )

    class Meta:
        ordering = ('-order',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# class Ingredient(Model):
#     name = CharField(verbose_name='Наименование', max_length=50)
#     measurement_unit = CharField(
#         verbose_name='Единица измерения',
#         max_length=30,
#     )
#     amount = PositiveSmallIntegerField(
#         verbose_name='Количество',
#         validators=(
#             MinValueValidator(1),
#         ),
#     )

#     class Meta:
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'Ингредиенты'

#     def __str__(self):
#         return self.name


class Position(Model):
    name = CharField(verbose_name='Наименование', max_length=50)
    price = PositiveSmallIntegerField(verbose_name='Цена')
    new = BooleanField(verbose_name='Новинка!', default=False)
    text = TextField(verbose_name='Описание')
    ingredients = CharField(verbose_name='Ингредиенты', max_length=1024)
    # ingredients = ManyToManyField(
    #     Ingredient,
    #     verbose_name='Ингредиенты',
    #     related_name='positions',
    # )
    category = ManyToManyField(
        Category,
        verbose_name='Категория',
        related_name='positions',
    )
    image = ImageField(
        verbose_name='Фото',
        upload_to='position',
        blank=True,
        null=True,
    )

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


class PositionForShopingCart(Model):
    position = ForeignKey(
        Position,
        verbose_name='Позиция',
        on_delete=CASCADE,
    )
    amount = PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(1),
        )
    )


class ShoppingCart(Model):
    positions_in_cart = ManyToManyField(
        PositionForShopingCart,
        verbose_name='Позиция',
    )
    all_amount = IntegerField(verbose_name='Цена в итоге')
    name_user = CharField(verbose_name='Клиент', max_length=100)
    phone = CharField(verbose_name='Номер телефона', max_length=12)
    email = EmailField(verbose_name='Почта', max_length=255)
    address = CharField(verbose_name='Место мероприятия', max_length=1024)
    date_start = DateTimeField(verbose_name='Дата мероприятия')
    comment = CharField(verbose_name='Комментарий', max_length=1024)
    pub_date = DateTimeField(
        verbose_name='Дата создания заявки',
        auto_now=True,
    )

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
