"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from social_network.api import *

from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

router = DefaultRouter()

router.register("profile", UserProfileViewSet, basename="profile")
router.register("basement", BasementViewSet, basename="basement")
router.register("user_basement", UserBasementViewSet, basename="user_basement")
router.register("child", ChildViewSet, basename="child")
router.register("post", PostViewSet, basename="post")
router.register("post_photo", PostPhotoViewSet, basename="post_photo")
router.register("child_photo", ChildPhotoViewSet, basename="chid_photo")
router.register("comment", CommentViewSet, basename="comment")
router.register("post_like", PostLikeViewSet, basename="post_like")
router.register("comment_like", CommentLikeViewSet, basename="comment_like")
router.register("reaction", ReactionViewSet, basename="reaction")
router.register("post_reaction", PostReactionViewSet, basename="post_reaction")
router.register("generate_data", GenerateDataViewSet, basename="generate_data")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/logout/', TokenBlacklistView.as_view()),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
