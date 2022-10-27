from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class EmailOrPhoneNumberBackend(BaseBackend):

    def get_user_by_password_or_phone_number(self, username):
        try:
            user = User.objects.get(Q(Q(phone_number=username) | Q(email=username)))
        except User.DoesNotExist:
            user = None
        return user

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        user = self.get_user_by_password_or_phone_number(username)

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None