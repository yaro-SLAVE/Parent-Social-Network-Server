from rest_framework import serializers

from social_network.models import *
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['password'] = make_password(password)
        validated_data['is_active'] = True
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        

        return super().update(instance, validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False, required = False)

    class Meta:
        model = UserProfile
        fields = "__all__"

class BasementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basement
        fields = "__all__"

class UserBasementSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False, required = False)
    basement = serializers.PrimaryKeyRelatedField(queryset = Basement.objects.all(), read_only = False, required = False)

    class Meta:
        model = UserBasement
        fields = "__all__"

class ChildSerializer(serializers.ModelSerializer):
    basement = serializers.PrimaryKeyRelatedField(queryset = Basement.objects.all(), read_only = False, required = False)

    class Meta:
        model = Child
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False, required = False)

    class Meta:
        model = Post
        fields = "__all__"

class PostPhotoSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset = Post.objects.all(), read_only = False, required = False)

    class Meta:
        model = PostPhoto
        fields = "__all__"

class ChildPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.PrimaryKeyRelatedField(queryset = PostPhoto.objects.all(), read_only = False, required = False)
    child = serializers.PrimaryKeyRelatedField(queryset = Child.objects.all(), read_only = False, required = False)

    class Meta:
        model = ChildPhoto
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset = Post.objects.all(), read_only = False, required = False)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False, required = False)

    class Meta:
        model = Comment
        fields = "__all__"

class PostLikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset = Post.objects.all(), read_only = False, required = False)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False, required = False)

    class Meta:
        model = PostLike
        fields = "__all__"

class CommentLikeSerializer(serializers.ModelSerializer):
    comment = serializers.PrimaryKeyRelatedField(queryset = Comment.objects.all(), read_only = False, required = False)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False, required = False)

    class Meta:
        model = CommentLike
        fields = "__all__"

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"

class PostReactionSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset = Post.objects.all(), read_only = False, required = False)
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only = False, required = False)
    reaction = serializers.PrimaryKeyRelatedField(queryset = Reaction.objects.all(), read_only = False, required = False)

    class Meta:
        model = Comment
        fields = "__all__"