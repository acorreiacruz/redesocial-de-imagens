from rest_framework.mixins import (
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from ..models import Profile
from ..serializers import (
    ProfileSerializer
)


class ProfileViewSet(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ["get", "patch", "options", "head"]
    permission_classes = [IsAuthenticated, ]
