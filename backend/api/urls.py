from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, CategoriesViewSet

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoriesViewSet, 'categories')
router.register('ingredients', IngredientsViewSet, 'ingredients')

urlpatterns = [
    path('', include(router.urls))
]
