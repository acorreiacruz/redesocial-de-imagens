from django.db import models
from .user import User


class Following(models.Model):
    class Meta:
        verbose_name = "Following"
        verbose_name_plural = "Following"
        ordering = ("-id",)
        db_table = "following"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"User {self.user.username} following {self.follower.username}"