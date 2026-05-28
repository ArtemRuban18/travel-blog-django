from django.contrib import admin
from .models import Likes

@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'content_id']
    list_filter = ['user','content_id']
    search_fields = ['user']