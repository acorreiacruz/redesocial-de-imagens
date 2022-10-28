from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ["post", "patch", "get", "head", "options", "delete"]

    def get_object(self, *args, **kwargs):
        print(self.kwargs)
        return super().get_object(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)







