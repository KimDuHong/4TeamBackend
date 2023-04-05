from django.contrib import admin
from .models import Feedlike, Commentlike


@admin.register(Feedlike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("pk",)


@admin.register(Commentlike)
class CommonlikeAdmin(admin.ModelAdmin):
    list_display = ("pk",)
