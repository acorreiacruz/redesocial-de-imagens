from django.db import models
from .post import Post
from .user import User


class Remark(models.Model):
    class Meta:
        verbose_name = "Remark"
        verbose_name_plural = "Remarks"
        ordering = ("-id",)
        db_table = "remarks"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=2200, null=False, blank=False)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Remark {self.id} by {self.user.username} on post {self.post.id}"

    @property
    def username(self):
        return self.user.username

    @property
    def post_id(self):
        return self.user.username
