from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import BasePermission 

from social_network.models import *
from social_network.serializers import *

from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from faker import Faker

from datetime import datetime
from datetime import timedelta

import random

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

class GenerateDataViewSet(
    GenericViewSet,
    mixins.CreateModelMixin
):

    def get_serializer_class(self):
        if self.action == "generate_users":
            return GenerateUsersSerializer

    @action(url_path="users", methods=["POST"], detail = False)
    def generate_users(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)
        
    
    @action(url_path="basements", methods=["POST"], detail = False)
    def generate_basements(self, *args, **options):
        fakers_count = self.request["fakers_count"]

        fake = Faker(['ru_RU'])

        for _ in range(fakers_count / 2):
            BasementSerializer.create(
                address = fake.street_address(),
                capacity = fake.random_number(digits=27)
            )
        
    @action(url_path="childs", methods=["POST"], detail = False)
    def generate_childs(self, *args, **options):
        fakers_count = self.request["fakers_count"]

        fake = Faker(['ru_RU'])

        parents_count = UserProfile.objects.count()
        basements_count = Basement.objects.count()

        for i in range(fakers_count / 2):

            parent_1 = parents_count - fakers_count + 1 + i
            parent_2 = parents_count - fakers_count / 2 + 1 + i
            current_basement = basements_count - fakers_count / 2 + 1 +i

            UserBasementSerializer.create(
                user = parent_1,
                basement = current_basement
            )

            UserBasementSerializer.create(
                user = parent_2,
                basement = current_basement
            )

            min_age = max(
                UserProfile.objects.get(parent_1).user.birth_date,
                UserProfile.objects.get(parent_2).user.birth_date
            )

            rand = random.randint(0, 1)

            first_name = ""

            if rand == 0:
                first_name = fake.first_name_male()
            else:
                first_name = fake.first_name_female()

            ChildSerializer.create(
                first_name = first_name,
                birth_date = fake.date_between_dates(
                    min_age - timedelta(days = 18 * 365),
                    min_age
                ),
                basement = current_basement
            )