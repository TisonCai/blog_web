from django.contrib import admin
from .models import Comment
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

# Register your models here.
@admin.register(Comment,site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target','content','nickname','website','create_time',)
    fields = ('target', 'content', 'nickname', 'website',)