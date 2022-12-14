from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


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
