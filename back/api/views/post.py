from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ..models import Post
from ..serializers import (
    LikesSerializer,
    PostRemarksSerializer,
    PostSerializer,
)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get", ], url_path="remarks", url_name="remarks")
    def list_post_remarks(self, *args, **kwargs):
        serializer = PostRemarksSerializer(
            instance=self.get_object(), many=False,
            context={"request": self.request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get", ], url_path="likes", url_name="likes")
    def list_post_likes(self, *args, **kwargs):
        serializer = LikesSerializer(
            instance=self.get_object(), many=False,
            context={"request": self.request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)