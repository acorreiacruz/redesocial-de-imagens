from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from api.models.following import Following
from .serializers import (
    PostSerializer,
    ProfileSerializer,
    RemarkSerializer,
    UserSerializer,
    PostLikeSerializer,
    PostRemarksSerializer,
    LikesSerializer,
    UserPostsListSerializer,
    UserFollowingSerializer,
    UserFollowersSerializer
)
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Profile, Post, PostLike, Remark, Following
from rest_framework.decorators import action


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
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
            return [AllowAny(),]
        return super().get_permissions(*args, **kwargs)

    @action(detail=False,url_path="me")
    def me(self, *args, **kwargs):
        object = self.get_object()
        serializer = self.serializer_class(object, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=["get",], detail=False, url_path="following", url_name="following")
    def list_user_following(self, *args, **kwargs):
        serializer = UserFollowingSerializer(instance=self.request.user, many=False, context={"request": self.request})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class ProfileViewSet(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', "patch", "options", "head"]


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)







