from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ingredient, Category
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import IngredientSerializer, CategorySerializer


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
