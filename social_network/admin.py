from django.contrib import admin
from social_network.models import Reaction

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ["id", "reaction_name", "reaction"]
