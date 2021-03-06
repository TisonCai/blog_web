from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property

# from login.models import MyUser
import mistune
# Create your models here.
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE, '删除')
    ]

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    desc = models.CharField(max_length=2020,verbose_name='分类描述',default='')

    def link_post_count(self):
        return Post.objects.filter(category_id=self.id).count()

    @staticmethod
    def get_navs():
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

    @staticmethod
    def get_defalut():
        cache = Category.objects.filter(name='未分类')
        if cache:
            return cache
        category = Category()
        category.name = '未分类'
        category.save()
        return category

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'
        ordering = ['-id']



class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE, '删除')
    ]

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    desc = models.CharField(max_length=2020, verbose_name='标签描述', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'



class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = [
        (STATUS_NORMAL,'正常'),
        (STATUS_DRAFT, '草稿'),
        (STATUS_DELETE, '删除')
    ]

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024,blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文',help_text='正文必须为Markdown格式')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='分类')
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    owner = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='作者')

    is_md = models.BooleanField(default=False,verbose_name='使用markdown语法')
    content_html = models.TextField(verbose_name='正文html格式', blank=True, editable=False)
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)


    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name',flat=True))

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=Post.STATUS_NORMAL).order_by('-pv')


    @staticmethod
    def get_by_owner(owner_id):
        try:
            user = User.objects.get(id=owner_id)
        except Tag.DoesNotExist:
            user = None
            post_list = []
        else:
            post_list = user.post_set.filter(status=Post.STATUS_NORMAL)

        return post_list,user


    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')

        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = Post.objects.filter(category_id=category_id)

        return post_list, category

    @staticmethod
    def lastes_posts():
        queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
        return queryset

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
            super(Post, self).save(force_insert=force_insert,
                     force_update=force_update,
                     using=using,
                     update_fields=update_fields)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']