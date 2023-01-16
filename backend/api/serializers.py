import phonenumbers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer, SerializerMethodField,
                                        ValidationError)
from rest_framework.validators import UniqueValidator
from users.models import CallMe, Contact, Link

# from .models import (Category, Ingredient, Position, PositionForShopingCart,
#                      ShoppingCart)
from .models import Category, Position, PositionForShopingCart, ShoppingCart

User = get_user_model()


# class ApiUserCreateSerializer(UserCreateSerializer):
#     username = CharField(
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )

#     class Meta:
#         fields = '__all__'
#         model = User
#         extra_kwargs = {'password': {'write_only': True}}


# class ApiUserSerializer(UserSerializer):

#     class Meta:
#         fields = '__all__'
#         model = User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# class IngredientSerializer(ModelSerializer):
#     amount = IntegerField()

#     class Meta:
#         model = Ingredient
#         fields = '__all__'


class PositionViewSerializer(ModelSerializer):
    # ingredients = SerializerMethodField(
    #     read_only=True,
    #     source='get_ingredients',
    # )

    class Meta:
        model = Position
        fields = '__all__'

    # def get_ingredients(self, obj):
    #     return IngredientSerializer(
    #         Ingredient.objects.filter(positions=obj),
    #         many=True,
    #     ).data


# class PositionCreateSerializer(ModelSerializer):
#    ingredients = IngredientSerializer(many=True)
#     image = Base64ImageField()

#     class Meta:
#         fields = '__all__'
#         model = Position

#     @staticmethod
#     def create_ingredients(ingredients, position):
#         for ingredient in ingredients:
#             new_ingredient = Ingredient.objects.create(
#                 name=ingredient['name'],
#                 measurement_unit=ingredient['measurement_unit'],
#                 amount=ingredient['amount']
#             )
#             position.ingredients.add(new_ingredient)

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients', None)
#         categories = validated_data.pop('category', None)
#         position = Position.objects.create(**validated_data)
#         self.create_ingredients(ingredients, position)
#         position.category.set(categories)
#         return position

#     def update(self, instance, validated_data):
#         Ingredient.objects.filter(positions=instance).delete()
#         ingredients = validated_data.pop('ingredients', None)
#         self.create_ingredients(ingredients, instance)
#         for category in instance.category.all():
#             instance.category.remove(category)
#         categories = validated_data.pop('category', None)
#         instance.category.set(categories)
#         return super().update(instance, validated_data)


class PositionForShopingCartSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = PositionForShopingCart


class ShoppingCartSerializer(ModelSerializer):
    positions_in_cart = PositionForShopingCartSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = ShoppingCart

    def validate_phone(self, value):
        new_number = phonenumbers.parse(value, "RU")
        if phonenumbers.is_valid_number(new_number) is False:
            raise ValidationError('Поле телефона не корректное')
        # if len(value) != 11:
        #     raise ValidationError('Поле телефона должно состоять из 11 цифр')
        return value

    @staticmethod
    def create_positions_for_card(shopping_cart, positions):
        for position in positions:
            position_with_amount = PositionForShopingCart.objects.create(
                position=position['position'],
                amount=position['amount']
            )
            shopping_cart.positions_in_cart.add(position_with_amount)

    def create(self, validated_data):
        positions = validated_data.pop('positions_in_cart', None)
        shopping_cart = ShoppingCart.objects.create(**validated_data)
        self.create_positions_for_card(shopping_cart, positions)
        return shopping_cart

    # # def update(self, instance, validated_data):
    # #     for position in instance.positions_in_cart.all():
    # #         instance.positions_in_cart.remove(position)
    # #         position.delete()
    # #     positions = validated_data.pop('positions_in_cart', None)
    # #     self.create_positions_for_card(instance, positions)
    # #     return super().update(instance, validated_data)


class LinkSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Link


class ContactSerializer(ModelSerializer):
    links = LinkSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Contact

    # def validate_phone(self, value):
    #     new_number = phonenumbers.parse(value, "RU")
    #     if phonenumbers.is_valid_number(new_number) is False:
    #         raise ValidationError('Поле телефона не корректное')
    #     # if len(value) != 11:
    #     #     raise ValidationError('Поле телефона должно состоять из 11 цифр')
    #     return value

    # @staticmethod
    # def create_link(contact, links):
    #     for link in links:
    #         new_link = Link.objects.create(
    #             link=link['link']
    #         )
    #         contact.links.add(new_link)

    # def create(self, validated_data):
    #     links = validated_data.pop('links', None)
    #     contact = Contact.objects.create(**validated_data)
    #     self.create_link(contact, links)
    #     return contact

    # def update(self, instance, validated_data):
    #     for link in instance.links.all():
    #         instance.links.remove(link)
    #         link.delete()
    #     links = validated_data.pop('links', None)
    #     self.create_link(instance, links)
    #     return super().update(instance, validated_data)


# class PositionCreateSerializer(ModelSerializer):
#     ingredients = IngredientSerializer(many=True)
#     image = Base64ImageField()

#     class Meta:
#         fields = '__all__'
#         model = Position

#     @staticmethod
#     def create_ingredients(ingredients, position):
#         for ingredient in ingredients:
#             new_ingredient = Ingredient.objects.create(
#                 name=ingredient['name'],
#                 measurement_unit=ingredient['measurement_unit'],
#                 amount=ingredient['amount']
#             )
#             position.ingredients.add(new_ingredient)

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients', None)
#         categories = validated_data.pop('category', None)
#         position = Position.objects.create(**validated_data)
#         self.create_ingredients(ingredients, position)
#         position.category.set(categories)
#         return position

#     def update(self, instance, validated_data):
#         Ingredient.objects.filter(positions=instance).delete()
#         ingredients = validated_data.pop('ingredients', None)
#         self.create_ingredients(ingredients, instance)
#         for category in instance.category.all():
#             instance.category.remove(category)
#         categories = validated_data.pop('category', None)
#         instance.category.set(categories)
#         return super().update(instance, validated_data)


class CallMeSerializer(ModelSerializer):
    phone = CharField()
    comment = CharField()

    class Meta:
        fields = '__all__'
        model = CallMe

    def validate_phone(self, value):
        new_number = phonenumbers.parse(value, "RU")
        if phonenumbers.is_valid_number(new_number) is False:
            raise ValidationError('Поле телефона не корректное')
        # if len(value) != 11:
        #     raise ValidationError('Поле телефона должно состоять из 11 цифр')
        return value
