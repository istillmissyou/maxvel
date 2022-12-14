from django.contrib import admin

from .models import Position, Ingredient, Category, ImagePositions


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'price',
        # 'category',
        'amount',
        # 'ingredients',
        # 'images',
        'text',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
        'amount',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


class ImagePositionsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'image',
    )


admin.site.register(ImagePositions, ImagePositionsAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
