from django.db import models
from .user import User


class Profile(models.Model):
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ("-id",)
        db_table = "profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profiles/photos/%Y/%m/%d/")
    biography = models.CharField(max_length=150, blank=True, null=False)
    is_private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Profile of: {self.user.username}"

    @property
    def username(self):
        return self.user.username