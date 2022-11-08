from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from api.models.remark import Remark
from .models import Following, Post, PostLike, Profile, User


class CustomJWTSerializer(TokenObtainPairSerializer):
    username_field = "authentication_field"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
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
            "followers",
        ]
        read_only_fields = ["following", "followers"]

    user = serializers.HyperlinkedRelatedField(
        many=False, view_name="api:api-user-detail", read_only=True
    )


class RemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remark
        fields = [
            "id",
            "username",
            "user",
            "text",
            "likes",
            "updated_at",
            "post_id"
        ]
        read_only_fields = ["likes", "updated_at", "id", "username"]
    post_id = serializers.IntegerField()
    user = serializers.HyperlinkedRelatedField(
        many=False, view_name="api:api-user-detail",
        read_only=True
    )

    def create(self, validated_data):
        user = validated_data.get("user")
        post = get_object_or_404(
            Post.objects.all(),
            id=validated_data.get("post_id")
        )
        text = validated_data.get("text")
        return Remark.objects.create(
            user=user, post=post, text=text
        )

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "photo", "text", "likes", "updated_at"]
        read_only_fields = ["likes", "updated_at"]

    user = serializers.HyperlinkedRelatedField(
        many=False, view_name="api:api-user-detail", read_only=True
    )


class PostRemarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["remarks"]

    remarks = RemarkSerializer(many=True)


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["user", "username", "post_id"]

    post_id = serializers.IntegerField(write_only=True)
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="api:api-user-detail",
        queryset=User.objects.all()
    )

    def create(self, validated_data):
        user = validated_data.get('user')
        post = get_object_or_404(
            Post.objects.all(),
            id=validated_data.get("post_id")
        )
        return PostLike.objects.create(user=user, post=post)


class UserPostsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["posts"]

    posts = PostSerializer(many=True)


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["postlikes"]

    postlikes = PostLikeSerializer(many=True)


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ["user", "created_at"]

    user = serializers.HyperlinkedRelatedField(
        many=False, view_name="api:api-user-detail",
        queryset=User.objects.all()
    )


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["following",]

    following = FollowingSerializer(many=True)


class UserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["followers",]

    followers = FollowingSerializer(many=True)