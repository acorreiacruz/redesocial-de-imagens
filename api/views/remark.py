from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..models import Remark
from ..serializers import (
    RemarkSerializer
)


class RemarkViewSet(
    GenericViewSet, UpdateModelMixin,
    DestroyModelMixin, CreateModelMixin
):
    queryset = Remark.objects.all()
    serializer_class = RemarkSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["post", "patch", "head", "options", "delete"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
