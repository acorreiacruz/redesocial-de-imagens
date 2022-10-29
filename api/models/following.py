from django.db import models
from .user import User
from django.core.exceptions import ValidationError


class Following(models.Model):
    class Meta:
        verbose_name = "Following"
        verbose_name_plural = "Following"
        ordering = ("-id",)
        db_table = "following"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"],
                name="user_cant_follow_other_twice"
            )
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        errors = {}
        if self.user.id == self.following.id:
            errors['user'] = "A user can't follow yourself !"
            errors['following'] = "A user can't be followed by yoursel !"
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.user.id == self.following.id:
            raise ValueError("A user can't follow yourself !")
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"User {self.user.username} following {self.following.username}"