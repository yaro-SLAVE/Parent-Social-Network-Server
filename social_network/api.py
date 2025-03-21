from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import BasePermission 

from social_network.models import *
from social_network.serializers import *

from rest_framework.permissions import IsAuthenticated

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