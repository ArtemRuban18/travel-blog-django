from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio','image_preview', 'user_email', 'created_at']
    search_fields = ['user', 'user_email']

    def image_preview(self, obj):
        if obj.image:
            return obj.image.url
        return "No image"
    
    def user_email(self, obj):
        return obj.user.email

