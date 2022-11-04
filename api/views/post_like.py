from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import PostLike
from ..serializers import (
    PostLikeSerializer
)


class PostLikeViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["post", "head", "options", "delete"]

    def destroy(self, request, *args, **kwargs):
        postlike = get_object_or_404(
            self.get_queryset(),
            post_id=kwargs.get("pk"),
            user=self.request.user
        )
        postlike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
