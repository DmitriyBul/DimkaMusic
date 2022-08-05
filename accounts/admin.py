from django.contrib import admin
from .models import Profile, TelegramUserRelation


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]


@admin.register(TelegramUserRelation)
class TelegramUserRelationAdmin(admin.ModelAdmin):
    list_display = ['user', 'telegram_id']
