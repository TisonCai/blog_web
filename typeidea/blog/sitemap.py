from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'always'
    protocol = 'http'
    priority = 1.0

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def location(self, obj):
        return reverse('post-detail',args=[obj.pk])

    def lastmod(self, obj):
        return obj.create_time

