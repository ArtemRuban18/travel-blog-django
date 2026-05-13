from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_querysqt().filter(status = Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
    category = models.ForeignKey('Category', on_delete= models.CASCADE, related_name = 'posts')
    image = models.ImageField(upload_to='posts/%Y/%m/%d', blank = True)
    status = models.CharField(max_length = 2, choices = Status.choices, default = Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add = True)
    publish = models.DateTimeField(default = timezone.now)
    views = models.PositiveBigIntegerField(default = 0)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields = ['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.slug])
    
class Category(models.Model):
    name = models.CharField(max_length = 250, unique = True, blank = False)
    slug = models.SlugField(max_length = 250, unique = True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts:post_list_by_category', args = [self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
    text = models.CharField(blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.text