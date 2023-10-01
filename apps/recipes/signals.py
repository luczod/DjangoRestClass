
import os
from recipes.models import Recipe
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError) as e:
        print(e)


@receiver(pre_delete, sender=Recipe)
def recipe_post_signal(sender, instance,  *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return
