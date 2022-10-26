from django.db import models
from .user import User
from .remark import Remark


class RemarkLike(models.Model):
    class Meta:
        verbose_name = "RemarkLike"
        verbose_name_plural = "RemarkLikes"
        ordering = ("-id",)
        db_table = "remark_likes"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remark = models.ForeignKey(Remark, on_delete=models.CASCADE)

    def __str__(self):
        return f"Remark {self.id} liked by {self.user.username}"