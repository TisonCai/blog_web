from django.contrib import admin
from .models import Post,Category,Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry

# Register your models here.
class PostInline(admin.TabularInline):
    model = Post
    fields = ('title','desc',)
    extra = 1

@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]

    list_display = ('name','status','is_nav','create_time','post_count')
    fields = ('name','status','is_nav')

    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin,self).save_model(request, obj, form, change)



@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','create_time')
    fields = ('name','status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin,self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    # '''自定义过滤器只展示当前用户分类'''
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        print('哈哈哈')
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset



@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = ['title','category','status','create_time','operator','owner']
    list_display_links = []
    list_filter = [CategoryOwnerFilter]

    # exclude = ('owner',)

    search_fields = ['title','category__name']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    # fields = (('category','title'), 'desc','status','content','tag')
    fieldsets = (
        ('基础配置',{
            'description': '基础配置描述',
            'fields': (
                ('title','category'),
                'status',
            )
        }),
        ('内容',{
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息',{
            'fields': (
                'tag',
            ),
            'classes': ('wide',),

        })
    )
    filter_horizontal = ('tag',)

    def operator(self,obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('cus_admin:blog_post_change', args=(obj.id,)))
    operator.short_description = '操作'

    def has_add_permission(self, request):
        '''做逻辑判断用户是否有权限增加文章'''
        return True

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin,self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super(PostAdmin,self).get_queryset(request)
    #     return qs.filter(owner=request.user)

@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']

















