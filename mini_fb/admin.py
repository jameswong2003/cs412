from django.contrib import admin
from .models import Profile, StatusMessage, Image, Friend

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'email')

@admin.register(StatusMessage)
class StatusMessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'message', 'timestamp')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_file', 'timestamp', 'status_message')

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('profile1', 'profile2', 'timestamp')