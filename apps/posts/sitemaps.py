from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    frequency = 'weekly'
    priority = 0.9

    def itenms(self):
        return Post.published.all()
    
    def lastmod(self,obj):
        return obj.updated