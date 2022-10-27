from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, User, Tag, Remark, RemarkLike, Post, PostLike, Following


@admin.register(User)
class UserAdminConfig(UserAdmin):
    list_display = "id", "username", "email", "is_active", "is_staff"
    list_display_links = ("username", "email")
    list_per_page = 25
    fieldsets = (
        (
            "Authentication Fields",
            {
                "fields": ("username","email", "phone_number"),
            }
        ),
        (
            None,
            {
                "fields": ("password",),
            }
        ),
        (
            "Personal Info",
            {
                "fields": ("first_name","last_name"),
            }
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                ),
            }
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login","date_joined"),
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdminConfig(admin.ModelAdmin):
    list_display = "id", "username", "is_private"
    list_per_page = 25
    list_display_links = ("id",)
    list_filter = ("is_private",)


@admin.register(Remark)
class RemarkAdminConfig(admin.ModelAdmin):
    list_display = "id", "username", "post_id", "likes", "created_at"
    list_display_links = "id", "username"
    list_per_page = 25


@admin.register(RemarkLike)
class RemarkLikeAdminConfig(admin.ModelAdmin):
    list_display = "id", "remark_id", "post_id", "liked_by", "user_id"
    list_display_links = "id", "liked_by"
    list_per_page = 25


@admin.register(Post)
class PostAdminConfig(admin.ModelAdmin):
    list_display = "id", "username", "likes", "created_at"
    list_display_links = "id", "username"
    list_per_page = 25


@admin.register(PostLike)
class PostLikeAdminConfig(admin.ModelAdmin):
    list_display = "id", "user", "post_id"
    list_display_links = "user", "post_id"
    list_per_page = 25


@admin.register(Following)
class FollowingAdminConfig(admin.ModelAdmin):
    list_display = "id", "user", "following", "created_at"
    list_display_links = "id" ,"user"
    search_fields = "user", "following"
    list_per_page = 25