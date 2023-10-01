from authors.models import Profile
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


# case user default mdoel was changed
User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(author=instance)
        profile.save()
