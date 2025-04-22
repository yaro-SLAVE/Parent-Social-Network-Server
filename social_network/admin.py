from django.contrib import admin
from social_network.models import Reaction, UserProfile

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ["id", "reaction_name", "reaction"]

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "logo", "birth_date"]
