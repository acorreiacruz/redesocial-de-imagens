from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from .models import Profile, User, PostLike
import os


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def delete_photo(instance):
    try:
        os.remove(instance.photo.path)
    except (ValueError, FileNotFoundError):
        pass


@receiver(pre_save, sender=Profile)
def update_profile_photo(sender, instance, *args, **kwargs):
    old_instance = Profile.objects.filter(id=instance.id).first()
    if not old_instance:
        return
    is_new = old_instance.photo != instance.photo
    if is_new:
        delete_photo(old_instance)


@receiver(pre_delete, sender=Profile)
def delete_profile_photo(sender, instance, *args, **kwargs):
    old_instance = Profile.objects.filter(id=instance.id).first()
    if old_instance:
        delete_photo(old_instance)


def increase_likes(instance):
    instance.likes += 1
    instance.save()
