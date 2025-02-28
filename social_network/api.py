from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from rest_framework.permissions import BasePermission 

from social_network.models import *
from social_network.serializers import *
from django.contrib.auth.models import User

from rest_framework.response import Response
from django.http import HttpResponse

from rest_framework.permissions import IsAuthenticated

from django.conf import settings

class UserViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class BasementViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Basement.objects.all()
    serializer_class = BasementSerializer

class UserBasementViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = UserBasement.objects.all()
    serializer_class = UserBasementSerializer

class ChildViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

class PostViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostPhotoViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer

class ChildPhotoViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = ChildPhoto.objects.all()
    serializer_class = ChildPhotoSerializer

class CommentViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostLikeViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

class CommentLikeViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

class ReactionViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

class PostReactionViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer