from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def index(request, *args, **kwargs):
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})
    return Response({'message': 'Это был GET-запрос!'})
