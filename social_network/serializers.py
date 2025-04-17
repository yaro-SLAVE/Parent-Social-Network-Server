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
        user = UserSerializer.create(validated_data)

        validated_data["user"] = user

        return super().create(validated_data)

    class Meta:
        model = UserProfile
        fields = "__all__"

class CreateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birth_date = serializers.DateField(required = False)

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            password = make_password(validated_data['password']),
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'], 
            is_active = True
        )

        if ('birth_date' in validated_data):
            profile = UserProfile.objects.create(
                user=user,
                birth_date=validated_data['birth_date']
            )
        else:
            profile = UserProfile.objects.create(
                user=user
            )

        return validated_data

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

    def create(self, validated_data):
        return super().create(validated_data)

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
        model = PostReaction
        fields = "__all__"

class GenerateUsersSerializer(serializers.Serializer):
    fakers_count = serializers.IntegerField()

    def create(self, validated_data):
        fakers_count = int(self.context["request"].data["fakers_count"])

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
        fakers_count = int(self.context["request"].data["fakers_count"])

        fake = Faker(['ru_RU'])

        for _ in range(int(fakers_count / 2)):
            Basement.objects.create(
                address = fake.street_address(),
                capacity = fake.random_int(5, 27, 1)
            )

        return validated_data
    
class GenerateChildrenSerializer(serializers.Serializer):
    fakers_count = serializers.IntegerField()

    def create(self, validated_data):
        fakers_count = int(self.context["request"].data["fakers_count"])

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
    
class GeneratePostsSerializer(serializers.Serializer):
    fakers_count = serializers.IntegerField()

    def create(self, validated_data):
        fakers_count = int(self.context["request"].data["fakers_count"])

        fake = Faker(['ru_RU'])

        parents_count = UserProfile.objects.count()
        children_count = Child.objects.count()

        parents = UserProfile.objects.all()
        children = Child.objects.all()

        for i in range(fakers_count):
            post = Post.objects.create(
                user = parents.get(id=parents_count - fakers_count + 1 + i).user,
                title = fake.text(max_nb_chars=20),
                body = fake.text(max_nb_chars=250),
                create_time = fake.date_time_between_dates(datetime_start=datetime(2023, 4, 5).date())
            )

            rand = random.randint(1, 4)

            for _ in range(rand):
                post_photo = PostPhoto.objects.create(
                    post = post,
                    photo = fake.image_url(500, 800)
                )

                rand_count = random.randint(1, 2)

                for _ in range(rand_count):
                    child_id = random.randint(1, children_count)
                    ChildPhoto.objects.create(
                        photo = post_photo,
                        child = children.get(id=child_id)
                    )

            likes_count = random.randint(5, 100)

            for _ in range(likes_count):
                rand_parent = 0
                while (parents.get(id=rand_parent).DoesNotExist):
                    rand_parent = random.randint(1, parents_count)                

                PostLike.objects.create(
                    post = post,
                    user = parents.get(id=rand_parent).user,
                    date = fake.date_time_between_dates(datetime_start=post.create_time)
                )

            comment_rand = random.randint(1, 10)

            for _ in range(comment_rand):
                rand_parent = 0
                while (parents.get(id=rand_parent).DoesNotExist):
                    rand_parent = random.randint(1, parents_count) 

                comment = Comment.objects.create(
                    user = parents.get(id=rand_parent).user,
                    post = post,
                    body = fake.text(max_nb_chars=30),
                    date = fake.date_time_between_dates(datetime_start=post.create_time)
                )

                rand_likes = random.randint(0, 10)

                for _ in range(rand_likes):
                    rand_parent = 0
                while (parents.get(id=rand_parent).DoesNotExist):
                    rand_parent = random.randint(1, parents_count) 

                    CommentLike.objects.create(
                        comment = comment,
                        user = parents.get(id=rand_parent).user,
                        date = fake.date_time_between_dates(datetime_start=comment.date)
                    )

            rand_reactions = random.randint(1, 10)
            reactions = Reaction.objects.all()
            reactions_count = Reaction.objects.count()

            for _ in range(rand_reactions):
                rand_parent = 0
                while (parents.get(id=rand_parent).DoesNotExist):
                    rand_parent = random.randint(1, parents_count) 

                rand = random.randint(1, reactions_count)
                
                PostReaction.objects.create(
                    post = post,
                    user = parents.get(id=rand_parent).user,
                    reaction = reactions.get(id=rand),
                    date = fake.date_time_between_dates(datetime_start=post.create_time)
                )

        return validated_data