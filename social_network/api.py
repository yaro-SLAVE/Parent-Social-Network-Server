from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import BasePermission 

from social_network.models import *
from social_network.serializers import *

from rest_framework.permissions import IsAuthenticated

from django.db.models import Count

class UserProfileViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin
):
    queryset = UserProfile.objects.all()
    
    def get_serializer_class(self):
        if self.action == "create":
            return CreateProfileSerializer
        else:
            return UserProfileSerializer
        
    def get_queryset(self):
        print(len(super().get_queryset()))
        last_name = self.request.GET.get("last_name")
        user_ids = User.objects.filter(last_name__contains = last_name).all()
        queryset = super().get_queryset().filter(user__in = user_ids)
        print(len(queryset))
        return queryset

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

    def get_queryset(self):
        capacity = self.request.GET.get('capacity')
        print(capacity)
        return super().get_queryset().filter(capacity = capacity).annotate(Count("id")).order_by('-id__count')[:10]

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

    def get_queryset(self):
        return super().get_queryset().annotate(title_count = Count("title")).order_by('-title_count')[:50]

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

    def get_queryset(self):
        user_id = self.request.GET.get("user")
        user = User.objects.get(pk = user_id)
        return super().get_queryset().filter(user = user).annotate(Count("id")).order_by('-id__count')[:50]

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

    def get_queryset(self):
        return super().get_queryset().annotate(Count("id")).order_by('-id__count')[:30]

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

    def get_queryset(self):
        return super().get_queryset().annotate(Count("id")).order_by('-id__count')[:60]

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

    def get_queryset(self):
        return super().get_queryset().annotate(Count("id")).order_by('-id__count')[:30]

class GenerateDataViewSet(
    GenericViewSet,
    mixins.CreateModelMixin
):

    def get_serializer_class(self):
        if self.action == "generate_users":
            return GenerateUsersSerializer
        elif self.action == "generate_basements":
            return GenerateBasementsSerializer
        elif self.action == "generate_children":
            return GenerateChildrenSerializer
        elif self.action == "generate_posts":
            return GeneratePostsSerializer

    @action(url_path="users", methods=["POST"], detail = False)
    def generate_users(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)
        
    
    @action(url_path="basements", methods=["POST"], detail = False)
    def generate_basements(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)
        
    @action(url_path="children", methods=["POST"], detail = False)
    def generate_children(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)
    
    @action(url_path="posts", methods=["POST"], detail = False)
    def generate_posts(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)