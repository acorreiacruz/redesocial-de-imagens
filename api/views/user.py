from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
    ListModelMixin
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import User, Following
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from ..serializers import (
    UserFollowersSerializer,
    UserFollowingSerializer,
    UserSerializer,
)


class UserViewSet(
    GenericViewSet, CreateModelMixin,
    UpdateModelMixin, DestroyModelMixin, ListModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["post", "patch", "get", "head", "options", "delete"]

    def get_object(self):
        queryset = self.get_queryset()
        object = queryset.get(pk=self.request.user.pk)
        return object

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(pk=self.request.user.pk)

    def get_permissions(self, *args, **kwargs):
        if self.request.method == "POST":
            return [AllowAny(), ]
        return super().get_permissions(*args, **kwargs)

    @action(detail=False, url_path="me")
    def me(self, *args, **kwargs):
        object = self.get_object()
        serializer = self.serializer_class(object, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(
        methods=["get", ], detail=False, url_path="following", url_name="following")
    def list_user_following(self, *args, **kwargs):
        serializer = UserFollowingSerializer(
            instance=self.request.user, many=False,
            context={"request": self.request}
        )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["get", ], detail=False, url_path="followers", url_name="followers")
    def list_user_followers(self, *args, **kwargs):
        serializer = UserFollowersSerializer(
            instance=self.request.user, many=False,
            context={"request": self.request}
        )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def get_user_by_id(id):
    return get_object_or_404(User.objects.all(), id=id)


def user_already_following(user, following):
    return Following.objects.filter(user=user, following=following).exists()


@api_view(["get", ])
def follow_user(request, id1, id2):
    following = get_user_by_id(id2)
    if user_already_following(request.user, following):
        return Response(
            data={"detail": "Loged user already following this user!"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
    Following.objects.create(user=request.user, following=following)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["get", ])
def unfollow_user(request, id1, id2):
    following = get_object_or_404(User.objects.all(), id=id2)
    get_object_or_404(
        Following.objects.all(), user=request.user, following=following
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
