from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Tag, Post, Category
from config.models import Link
from comment.forms import CommentForm
from comment.models import Comment
from config.models import SideBar
from .adminforms import PostAddForm

from django.views.generic import DetailView,ListView,TemplateView
from django.shortcuts import get_object_or_404

from datetime import date
from django.core.cache import cache

from django.db.models import Q,F
# Create your views here.

def post_list(request,category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.lastes_posts()

    context = {
        'tag': tag,
        'category': category,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request,'blog/list.html',context=context)

class CommonViewMixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


# 首页
class IndexView(ListView):
    queryset = Post.lastes_posts()
    paginate_by = 8
    template_name = 'blog/list.html'
    context_object_name = 'post_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'keyword': ''
        })
        context.update(Category.get_navs())
        return context


# 搜索页
class SearchView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword','')
        })
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword')
        if  not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


# auhtor
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


# 分类页
class CategoryView(IndexView):
    pk_url_kwarg = 'category_id'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        '''k控制数据源'''
        '''重写queryset，根据分类设置'''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


# 标签页
class TagView(IndexView):
        def get_context_data(self, *, object_list=None, **kwargs):
            context = super(TagView, self).get_context_data(**kwargs)
            tag_id = self.kwargs.get('tag_id')
            tag = get_object_or_404(Tag, pk=tag_id)
            context.update({
                'tag': tag
            })
            return context

        def get_queryset(self):
            '''重写queryset，根据分类设置'''
            queryset = super().get_queryset()
            tag_id = self.kwargs.get('tag_id')
            print('kekeke')
            print(queryset)
            fliter = queryset.filter(tag=Tag.objects.get(id=tag_id))
            print(fliter)
            return fliter

# 文章详情页
class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.lastes_posts()
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request,*args, **kwargs)
        self.handle_vistor()
        return response


    def handle_vistor(self):
        increate_pv = True
        increate_uv = True
        # increate_pv = False
        # increate_uv = False
        # uid = self.request.uid
        # cacheKey_pv = 'pv:%s:%s' % (uid, self.request.path)
        # cacheKey_uv = 'uv:%s:%s:%s' % (uid,str(date.today()),self.request.path)
        # if not cache.get(cacheKey_pv):
        #     cache.set(cacheKey_pv, 1, 1 * 60)
        #     increate_pv = True
        #
        # if not cache.get(cacheKey_uv):
        #     cache.set(cacheKey_pv, 24, 1 * 60 * 60)
        #     increate_uv = True

        if increate_pv and increate_uv:
            Post.objects.filter(pv=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increate_pv:
            Post.objects.filter(pv=self.object.id).update(pv=F('pv') + 1)
        elif increate_uv:
            Post.objects.filter(pv=self.object.id).update(uv=F('uv') + 1)


class PostAddView(TemplateView):
    template_name = 'blog/addpost.html'

    def post(self, request, *args, **kwargs):
        addpost_form = PostAddForm(request.POST)
        if addpost_form.is_valid():
            data = addpost_form.cleaned_data
            post = Post()
            post.content = data.get('content')
            post.title = data.get('title')
            post.desc = data.get('desc')
            post.category = data.get('category')
            post.owner = data.get('owner')
            post.save()
            print('addpost表单有效')
            print(data)
            return redirect('/')
        else:
            print('addpost表单无效')
        return render(request, 'blog/addpost.html', locals())

    def get(self, request, *args, **kwargs):
        addpost_form = PostAddForm()
        return render(request, 'blog/addpost.html', locals())


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        return render(request, 'blog/detail.html', context={'post': post})
    except Post.DoesNotExist:
        post = None

    context = {
            'post': post,
            'sidebars': SideBar.get_all(),
        }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)



# 首页
class TestIndexView(ListView):
    queryset = Post.lastes_posts()
    paginate_by = 8
    template_name = 'blog/_index.html'
    context_object_name = 'post_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TestIndexView, self).get_context_data(**kwargs)
        tags = Tag.objects.filter(status=Tag.STATUS_NORMAL)
        categorys = Category.objects.filter(status=Category.STATUS_NORMAL)
        links = Link.objects.filter(status=Link.STATUS_NORMAL)
        context.update({
            'keyword': '',
            'tags': tags,
            'categorys': categorys,
            'links': links,
        })
        context.update(Category.get_navs())
        return context


class HotIndexView(ListView):
    queryset = Post.hot_posts()
    paginate_by = 8
    template_name = 'blog/_index.html'
    context_object_name = 'post_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HotIndexView, self).get_context_data(**kwargs)
        tags = Tag.objects.filter(status=Tag.STATUS_NORMAL)
        categorys = Category.objects.filter(status=Category.STATUS_NORMAL)
        links = Link.objects.filter(status=Link.STATUS_NORMAL)
        context.update({
            'keyword': '',
            'tags': tags,
            'categorys': categorys,
            'links': links,
        })
        context.update(Category.get_navs())
        return context


class SearchIndexView(ListView):
    queryset = Post.hot_posts()
    paginate_by = 8
    template_name = 'blog/_index.html'
    context_object_name = 'post_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchIndexView, self).get_context_data(**kwargs)
        tags = Tag.objects.filter(status=Tag.STATUS_NORMAL)
        categorys = Category.objects.filter(status=Category.STATUS_NORMAL)
        links = Link.objects.filter(status=Link.STATUS_NORMAL)
        context.update({
            'keyword': self.request.GET.get('keyword',''),
            'tags': tags,
            'categorys': categorys,
            'links': links,
        })
        return context

    def get_queryset(self):
        queryset = super(SearchIndexView, self).get_queryset()
        keyword = self.request.GET.get('keyword')
        if  not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))



class PostDetailIndexView(CommonViewMixin, DetailView):
    queryset = Post.lastes_posts()
    context_object_name = 'post'
    template_name = 'blog/_detail.html'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request,*args, **kwargs)
        self.handle_vistor()
        return response


    def handle_vistor(self):
        increate_pv = True
        increate_uv = True
        # increate_pv = False
        # increate_uv = False
        # uid = self.request.uid
        # cacheKey_pv = 'pv:%s:%s' % (uid, self.request.path)
        # cacheKey_uv = 'uv:%s:%s:%s' % (uid,str(date.today()),self.request.path)
        # if not cache.get(cacheKey_pv):
        #     cache.set(cacheKey_pv, 1, 1 * 60)
        #     increate_pv = True
        #
        # if not cache.get(cacheKey_uv):
        #     cache.set(cacheKey_pv, 24, 1 * 60 * 60)
        #     increate_uv = True
        if increate_pv and increate_uv:
            Post.objects.filter(pv=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increate_pv:
            Post.objects.filter(pv=self.object.id).update(pv=F('pv') + 1)
        elif increate_uv:
            Post.objects.filter(pv=self.object.id).update(uv=F('uv') + 1)



class CategoryIndexView(ListView):
    queryset = Post.lastes_posts()
    paginate_by = 8
    template_name = 'blog/_category.html'
    context_object_name = 'post_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryIndexView, self).get_context_data(**kwargs)
        tags = Tag.objects.filter(status=Tag.STATUS_NORMAL)
        categorys = Category.objects.filter(status=Category.STATUS_NORMAL)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        post_list = Post.get_by_category(category_id)[0]

        links = Link.objects.filter(status=Link.STATUS_NORMAL)
        context.update({
            'keyword': '',
            'tags': tags,
            'categorys': categorys,
            'links': links,
            'post_list': post_list,
            'category': category,
        })
        context.update(Category.get_navs())
        return context


class TagIndexView(ListView):
    queryset = Post.lastes_posts()
    paginate_by = 8
    template_name = 'blog/_tag.html'
    context_object_name = 'post_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagIndexView, self).get_context_data(**kwargs)
        tags = Tag.objects.filter(status=Tag.STATUS_NORMAL)
        categorys = Category.objects.filter(status=Category.STATUS_NORMAL)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        post_list = Post.get_by_tag(tag_id)[0]

        links = Link.objects.filter(status=Link.STATUS_NORMAL)
        context.update({
            'keyword': '',
            'tags': tags,
            'categorys': categorys,
            'links': links,
            'post_list': post_list,
            'tag': tag,
        })
        return context