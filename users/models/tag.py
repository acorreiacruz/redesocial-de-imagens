from django.db import models
from .post import Post
from django.utils.text import slugify


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ("-id",)
        db_table = "tags"

    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.SlugField(unique=True)
    post = models.ManyToManyField(Post, on_delete=models.SET_NULL, related_name="tags")

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if not self.slug:
            self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Tag {self.name} on post {self.post.name}"
