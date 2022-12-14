from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Category, Ingredient, Position, ImagePositions
from .serializers import (CategorySerializer, IngredientSerializer,
                          PositionCreateSerializer, PositionViewSerializer)


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class CategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PositionViewSerializer
        return PositionCreateSerializer

    def list(self, request, *args, **kwargs):
        category = self.request.query_params.get('category')
        if category is None:
            self.queryset = self.queryset.filter(new=True)
        else:
            self.queryset = self.queryset.filter(category=category)
        return super(PositionViewSet, self).list(self, request, *args, **kwargs)

    def perform_destroy(self, instance):
        Ingredient.objects.filter(positions=instance).delete()
        images_positions = ImagePositions.objects.filter(positions=instance)
        for image in images_positions:
            image.image.delete(save=True)
            image.delete()
        instance.delete()
