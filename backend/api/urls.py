from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CallMeViewSet, CategoriesViewSet, ContactViewSet,
                    PositionViewSet, ShoppingCartViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('position', PositionViewSet, basename='position')
router.register('shopping-card', ShoppingCartViewSet, basename='shopping-card')
router.register('contacts', ContactViewSet, basename='contacts')
router.register('call-me', CallMeViewSet, basename='call-me')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
]
