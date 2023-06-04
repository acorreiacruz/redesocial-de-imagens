from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views
from .serializers import CustomJWTSerializer

app_name = "api"

router = SimpleRouter()
router.register("users", views.UserViewSet, "api-user")
router.register("profiles", views.ProfileViewSet, "api-profile")
router.register("posts", views.PostViewSet, "api-post")
router.register("postlikes", views.PostLikeViewSet, "api-postlike")
router.register("remarks", views.RemarkViewSet, "api-remark")

urlpatterns = [
    path(
        "users/<int:id1>/follow/<int:id2>/",
        views.follow_user,
        name="follow_user"
    ),
    path(
        "users/<int:id1>/unfollow/<int:id2>/",
        views.unfollow_user,
        name="unfollow_user"
    ),
    path("", include(router.urls)),
    path(
        "token/",
        TokenObtainPairView.as_view(serializer_class=CustomJWTSerializer),
        name="token_obtain_pair_email",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path(
        "token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify"
    ),
]
