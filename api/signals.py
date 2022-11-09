from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from .models import Profile, User, PostLike, Post
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


def decrease_likes(instance):
    if instance.likes > 0:
        instance.likes -= 1
        instance.save()


def increase_publications(instance):
    instance.publications +=1
    instance.save()


def decrease_publications(instance):
    if instance.publications > 0:
        instance.publications -= 1
        instance.save()

@receiver(post_save, sender=PostLike)
def like_post(sender, instance, created, **kwargs):
    if created:
        increase_likes(instance.post)


@receiver(pre_delete, sender=PostLike)
def deslike_post(sender, instance, *args, **kwargs):
    decrease_likes(instance.post)


@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.get(pk=instance.user.id)
        increase_publications(profile)
