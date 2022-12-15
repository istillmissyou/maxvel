from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Category, Position


@receiver(pre_delete, sender=Category)
def delete_category(sender, instance, **kwargs):
    position_in_this_category = Position.objects.filter(category=instance)
    for position in position_in_this_category:
        if position.category.count() == 1:
            position.delete()
