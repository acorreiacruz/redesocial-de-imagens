from django.db import models
from .user import User
from .remark import Remark


class RemarkLike(models.Model):
    class Meta:
        verbose_name = "RemarkLike"
        verbose_name_plural = "RemarkLikes"
        ordering = ("-id",)
        db_table = "remark_likes"
        constraints = [
            models.UniqueConstraint(
                fields=["liked_by", "remark"],
                name="remark_cant_be_liked_twice_by_same_user"
            ),
        ]

    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    remark = models.ForeignKey(Remark, on_delete=models.CASCADE)

    def __str__(self):
        return f"Remark {self.id} liked by {self.liked_by.username}"

    @property
    def remark_id(self):
        return self.remark.pk

    @property
    def user_id(self):
        return self.liked_by.pk

    @property
    def post_id(self):
        return self.remark.post.pk