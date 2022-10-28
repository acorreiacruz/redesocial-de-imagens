from .models import User
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import User, Profile


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated,]
    http_method_names = ["post", "patch", "get", "head", "options", "delete"]

    def get_object(self, *args, **kwargs):
        return super().get_object(self, *args, **kwargs)


class ProfileViewSet(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', "patch", "options", "head"]







