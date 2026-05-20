from django.contrib import admin
from .models import Post, Category, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'slug', 
                    'body', 
                    'author', 
                    'category',
                    'image_preview',
                    'status',
                    'publish', 
                    'views',
                    'tags_list']
    list_filter = ['publish', 'category']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    readonly_fields = ['views']

    def tags_list(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())
    
    def image_preview(self, obj):
        if obj.image:
            return obj.image.url
        return "No image"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'text', 'created_at']
    list_filter = ['post']
    search_fields = ['post__title', 'user__username']