from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Category, Position


@receiver(pre_delete, sender=Category)
def delete_category(sender, instance, **kwargs):
    position_in_this_category = Position.objects.filter(category=instance)
    for position in position_in_this_category:
        for ingredient in position.ingredients.all():
            ingredient.delete()
        for image in position.images.all():
            image.image.delete()
            image.delete()
        position.delete()


@receiver(pre_delete, sender=Position)
def delete_position(sender, instance, **kwargs):
    for ingredient in instance.ingredients.all():
        ingredient.delete()
    for image in instance.images.all():
        image.image.delete()
        image.delete()


# @receiver(pre_save, sender=Position)
# def save_position(sender, instance, **kwargs):
#     if instance.pk is not None:
#         position = Position.objects.get(pk=instance.pk)
#         for ingredient_in_bd in position.ingredients.all():
#             for ingredient_in_instance in instance.ingredients.all():
#                 if ingredient_in_instance == ingredient_in_bd:
#                     ingredient.delete()
#         for image in instance.images.all():
#             image.image.delete()
#             image.delete()