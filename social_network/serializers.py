from rest_framework import serializers

from social_network.models import *
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password

from faker import Faker

from datetime import datetime
from datetime import timedelta

import random

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

    def create(self, validated_data):
        if (validated_data["user"] is None):
            user = UserSerializer.create(User, validated_data)

            validated_data["user"] = user.id

        return super().create(validated_data)

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

class GenerateUsersSerializer(serializers.Serializer):
    fakers_count = serializers.IntegerField()

    def create(self, validated_data):
        fakers_count = self.context["request"].data["fakers_count"]

        print(fakers_count)

        fake = Faker(['ru_RU'])

        current_date = datetime.now().date()

        age_days_max = 365 * 30
        age_days_min = 365 * 20

        for _ in range(int(fakers_count / 2)):
            user = User.objects.create(
                username = fake.user_name(),
                password = make_password(fake.password()),
                is_active = True,
                first_name = fake.first_name_male(),
                last_name = fake.last_name()
            )

            UserProfile.objects.create(
                user = user,
                birth_date = fake.date_between_dates(
                    current_date - timedelta(days = age_days_max),
                    current_date - timedelta(days = age_days_min)
                )
            )

        for _ in range(fakers_count - int(fakers_count / 2)):
            user = User.objects.create(
                username = fake.user_name(),
                password = make_password(fake.password()),
                is_active = True,
                first_name = fake.first_name_female(),
                last_name = fake.last_name()
            )

            UserProfile.objects.create(
                user = user,
                birth_date = fake.date_between_dates(
                    current_date - timedelta(days = age_days_max),
                    current_date - timedelta(days = age_days_min)
                )
            )

        return validated_data
    
class GenerateBasementsSerializer(serializers.Serializer):
    fakers_count = serializers.IntegerField()

    def create(self, validated_data):
        fakers_count = self.context["request"].data["fakers_count"]

        fake = Faker(['ru_RU'])

        for _ in range(int(fakers_count / 2)):
            Basement.objects.create(
                address = fake.street_address(),
                capacity = fake.random_int(5, 27, 1)
            )

        return validated_data
    
class GenerateChildssSerializer(serializers.Serializer):
    fakers_count = serializers.IntegerField()

    def create(self, validated_data):
        fakers_count = self.context["request"].data["fakers_count"]

        fake = Faker(['ru_RU'])

        parents_count = UserProfile.objects.count()
        basements_count = Basement.objects.count()

        users = UserProfile.objects.all()
        basements = Basement.objects.all()

        for i in range(int(fakers_count / 2)):

            parent_1 = parents_count - fakers_count + 1 + i
            parent_2 = parents_count - fakers_count / 2 + 1 + i
            current_basement = basements_count - fakers_count / 2 + 1 +i

            UserBasement.objects.create(
                user = users.get(id=parent_1).user,
                basement = basements.get(id=current_basement)
            )

            UserBasement.objects.create(
                user = users.get(id=parent_2).user,
                basement = basements.get(id=current_basement)
            )

            min_age = max(
                users.get(id=parent_1).birth_date,
                users.get(id=parent_2).birth_date
            )

            rand = random.randint(0, 1)

            first_name = ""
            gender = ""

            if rand == 0:
                first_name = fake.first_name_male()
                gender = "мужской"
            else:
                first_name = fake.first_name_female()
                gender = "женский"

            Child.objects.create(
                first_name = first_name,
                gender = gender,
                birth_date = fake.date_between_dates(
                    min_age + timedelta(days = 18 * 365),
                    datetime.now().date()
                ),
                basement = basements.get(id=current_basement)
            )

        return validated_data
    
