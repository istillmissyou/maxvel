from django.contrib import admin

# from .models import (Category, Ingredient, PositionForShopingCart, Position,
#                      ShoppingCart)
from .models import Category, Position, PositionForShopingCart, ShoppingCart


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


# class IngredientAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'name',
#         'measurement_unit',
#         'amount',
#     )


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'price',
        # 'category',
        # 'amount',
        # 'image',
        'text',
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        # 'positions',
        'all_amount',
        'name_user',
        'phone',
        'email',
        'address',
        'date_start',
        'comment',
        'pub_date',
    )


class PosithionForShopingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'position',
        'amount',
    )


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(PositionForShopingCart, PosithionForShopingCartAdmin)
