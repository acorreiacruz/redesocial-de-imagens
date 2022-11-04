from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Following, Post, PostLike, Profile, Remark, User
from .serializers import (
    LikesSerializer,
    PostLikeSerializer,
    PostRemarksSerializer,
    PostSerializer,
    ProfileSerializer,
    RemarkSerializer,
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

    @action(methods=["get",], detail=False, url_path="followers", url_name="followers")
    def list_user_followers(self, *args, **kwargs):
        serializer = UserFollowersSerializer(instance=self.request.user, many=False, context={"request": self.request})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ProfileViewSet(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', "patch", "options", "head"]
    permission_classes = [IsAuthenticated,]

    @action(methods=["get",], detail=False, url_name="user-posts", url_path="user/posts")
    def lis_user_posts(self, *args, **kwargs):
        serializer = UserPostsListSerializer(
            instance=self.request.user, many=False,
            context={"request": self.request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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

    @action(detail=True, methods=["get",],url_path="remarks",url_name="remarks")
    def list_post_remarks(self, *args, **kwargs):
        serializer = PostRemarksSerializer(instance=self.get_object(), many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get",], url_path="likes", url_name="likes")
    def list_post_likes(self, *args, **kwargs):
        serializer = LikesSerializer(instance=self.get_object(), many=False, context={"request":self.request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostLikeViewSet(ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ["post", "patch", "get", "head", "options", "delete"]


class RemarkViewSet(GenericViewSet, ListModelMixin, DestroyModelMixin, CreateModelMixin):
    queryset = Remark.objects.all()
    serializer_class = RemarkSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ["post", "patch", "get", "head", "options", "delete"]


@api_view(["get",])
def follow_user(request, id1, id2):
    following = get_object_or_404(
        User.objects.all(),
        id=id2
    )
    Following.objects.create(
        user=request.user,
        following=following
    )
    return Response(status=status.HTTP_201_CREATED)

@api_view(["get",])
def unfollow_user(request, id1, id2):
    following = get_object_or_404(
        User.objects.all(),
        id=id2
    )
    get_object_or_404(
        Following.objects.all(),
        user=request.user,
        following=following
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



