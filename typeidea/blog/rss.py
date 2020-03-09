from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Post

class CustomRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomRSSFeed, self).add_item_elements(handler,item)
        handler.addQuickElement('content:html',item['content_html'])

        

class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed
    title_template = 'Blog system'
    link = '/rss/'
    description_template = 'Blog system by Django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post-detail',args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html' : self.item_content_html(item)}

    def item_content_html(self, item):
        return item.content_html


