from django.contrib import admin

from .models import Position, IngredientsInPosition, Ingredient, Category


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'image',
        'price',
        # 'category',
        'amount',
        # 'ingredients',
        'text',
    )


class IngredientsInPositionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'position',
        'ingredient',
        'amount',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


admin.site.register(IngredientsInPosition, IngredientsInPositionAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
