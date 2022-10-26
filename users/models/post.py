from django.db import models
from .user import User


class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbone_name_plural = "Posts"
        ordering = ("-id",)
        db_table = "posts"

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        photo = models.ImageField(upload_to="posts/photos/%Y/%m/%d/")
        text = models.CharField(max_length=2200, null=False, blank=False)
        likes = models.PositiveIntegerField(default=0)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"Post of user:{self.user.username}"

        @property
        def username(self):
            return self.user.username