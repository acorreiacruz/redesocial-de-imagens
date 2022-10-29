from django.db import models
from .post import Post
from .user import User


class PostLike(models.Model):
    class Meta:
        verbose_name = "PostLike"
        verbose_name_plural = "PostLikes"
        ordering = ("-id",)
        db_table = "post_likes"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="user_cant_like_a_post_twice"
            )
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postlikes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postlikes")

    def __str__(self):
        return f"Post {self.id} liked by {self.user.username}"

    @property
    def username(self):
        return self.user.username

    @property
    def post_id(self):
        return self.post.id
