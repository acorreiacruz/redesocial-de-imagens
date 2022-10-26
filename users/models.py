from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):

    def __field_error(self, field, message):
        if not field:
            raise ValueError(message)

    def create_user(self, username, email, phone_number, password, **other_fields):
        self.__field_error(username,"A user must have a username !")
        self.__field_error(email,"A user must have a email address")
        self.__field_error(phone_number,"A user must have a phone number !")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            **other_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, phone_number, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        user = self.create_user(username, email, phone_number, password, **other_fields)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-id",)
        db_table = "users"

    first_name = models.CharField(max_length=150, blank=True, null=False)
    last_name = models.CharField(max_length=150, blank=True, null=False)
    username = models.CharField(max_length=150, blank=False, null=False, unique=True)
    email = models.CharField(max_length=150, blank=False, null=False, unique=True)
    phone_number = PhoneNumberField(blank=False, null=False, max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username","email"]

    def __str__(self):
        return self.username


class Profile(models.Model):
    class Meta:
        verbose_name = "Profile"
        verbone_name_plural = "Profiles"
        ordering = ("-id",)
        db_table = "profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profiles/photos/%Y/%m/%d/")
    biography = models.CharField(max_length=150, blank=True, null=False)

    def __str__(self) -> str:
        return f"Profile of: {self.user.username}"


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


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbone_name_plural = "Tags"
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


class PostLike(models.Model):
    class Meta:
        verbose_name = "PostLike"
        verbone_name_plural = "PostLikes"
        ordering = ("-id",)
        db_table = "posts_likes"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post {self.id} liked by {self.user.username}"

    @property
    def username(self):
        return self.user.username

    @property
    def post_id(self):
        return self.post.id



class Remark(models.Model):
    class Meta:
        verbose_name = "Remark"
        verbone_name_plural = "Remarks"
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


class RemarkLike(models.Model):
    class Meta:
        verbose_name = "RemarkLike"
        verbone_name_plural = "RemarkLikes"
        ordering = ("-id",)
        db_table = "remarks_likes"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remark = models.ForeignKey(Remark, on_delete=models.CASCADE)

    def __str__(self):
        return f"Remark {self.id} liked by {self.user.username}"

