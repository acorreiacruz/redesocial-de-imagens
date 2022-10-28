from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name",
            "username", "email", "phone_number", "password"
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(password=password, **validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "user",
            "photo",
            "biography",
            "is_private",
            "following",
            "followers"
        ]
        read_only_fields = ["following", "followers"]
    user = serializers.HyperlinkedRelatedField(
        many=False,view_name="api:api-user-detail",
        read_only=True
    )