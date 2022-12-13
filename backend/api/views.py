from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Category, Ingredient, Position
from .serializers import (CategorySerializer, IngredientSerializer,
                          RecipeSerializer)


@api_view(['GET'])
def index(request, *args, **kwargs):
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})
    return Response({'message': 'Это был GET-запрос!'})


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
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

