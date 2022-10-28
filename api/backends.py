from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class EmailOrPhoneNumberBackend(BaseBackend):
    def authenticate(self, request, authentication_field=None, password=None , username=None):
        try:
            user = User.objects.get(
                    Q(phone_number=authentication_field or username) | Q(email=authentication_field or username)
            )
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None