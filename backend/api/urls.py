from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, CategoriesViewSet, PositionViewSet, index

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoriesViewSet, 'categories')
router.register('ingredients', IngredientsViewSet, 'ingredients')
router.register('position', PositionViewSet, basename='position')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('index/', index),
]
