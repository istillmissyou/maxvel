from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category, Ingredient, Position, IngredientsInPosition
from .serializers import (CategorySerializer, IngredientSerializer,
                          RecipeSerializer, IngredientInRecipeSerializer)


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class IngredientInRecipeViewSet(ReadOnlyModelViewSet):
    queryset = IngredientsInPosition.objects.all()
    serializer_class = IngredientInRecipeSerializer
    pagination_class = None


class CategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class PositionViewSet(ReadOnlyModelViewSet):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        queryset = Position.objects.all()
        category = self.request.query_params.get('category')
        if category is None:
            return queryset.filter(new=True)
        return queryset.filter(category=category)
