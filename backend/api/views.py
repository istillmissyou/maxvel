from celery_task.task import (send_email_with_call_me,
                              send_email_with_shopping_card)
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)
from users.models import CallMe, Contact, Link

# from .models import Category, Ingredient, Position, ShoppingCart
from .models import Category, Position, ShoppingCart
# from .serializers import (CategorySerializer, ContactSerializer,
#                           PositionCreateSerializer, PositionViewSerializer,
#                           ShoppingCartSerializer)
from .serializers import (CallMeSerializer, CategorySerializer,
                          ContactSerializer, PositionViewSerializer,
                          ShoppingCartSerializer)

# class CategoriesViewSet(ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     pagination_class = None


# class PositionViewSet(ModelViewSet):
#     queryset = Position.objects.all()

#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return PositionViewSerializer
#         return PositionCreateSerializer

#     def list(self, request, *args, **kwargs):
#         category = self.request.query_params.get('category')
#         if category is None:
#             self.queryset = self.queryset.filter(new=True)
#         else:
#             self.queryset = self.queryset.filter(category=category)
#         return super().list(self, request, *args, **kwargs)

#     def perform_destroy(self, instance):
#         Ingredient.objects.filter(positions=instance).delete()
#         instance.delete()


# class ContactViewSet(ModelViewSet):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer

#     def perform_destroy(self, instance):
#         Link.objects.filter(contact=instance).delete()
#         instance.delete()


class CategoriesViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class PositionViewSet(ReadOnlyModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionViewSerializer

    def list(self, request, *args, **kwargs):
        category = self.request.query_params.get('category')
        if category is None:
            self.queryset = self.queryset.filter(new=True)
        else:
            self.queryset = self.queryset.filter(category=category)
        return super().list(self, request, *args, **kwargs)


class ShoppingCartViewSet(
            # generics.ListAPIView,
            generics.CreateAPIView,
            generics.RetrieveAPIView,
            GenericViewSet
        ):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def perform_create(self, serializer):
        shopping_card = serializer.save()
        send_email_with_shopping_card.delay(shopping_card.pk,)


class ContactViewSet(
            generics.ListAPIView,
            GenericViewSet
            ):
    serializer_class = ContactSerializer

    def list(self, request, *args, **kwargs):
        obj = get_object_or_404(Contact, pk=1)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    # def perform_destroy(self, instance):
    #     Link.objects.filter(contact=instance).delete()
    #     instance.delete()


class CallMeViewSet(
            generics.CreateAPIView,
            GenericViewSet
        ):
    queryset = CallMe.objects.all()
    serializer_class = CallMeSerializer

    def perform_create(self, serializer):
        call_me = serializer.save()
        send_email_with_call_me.delay(call_me.pk,)
