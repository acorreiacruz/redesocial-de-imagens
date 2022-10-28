from .models import User
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Profile


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


class ProfileViewSet(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', "patch", "options", "head"]







