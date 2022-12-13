from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Position
from .serializers import RecipeSerializer
from rest_framework import status, viewsets


@api_view(['GET'])
def index(request, *args, **kwargs):
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})
    return Response({'message': 'Это был GET-запрос!'})


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = RecipeSerializer