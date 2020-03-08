"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from typeidea.custom_site import custom_site
from blog.views import post_list, post_detail
from config.views import links
from comment.views import CommentView

from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static

from login.views import LoginView,RegisterView

from blog.apis import PostViewSet,CategoryViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
router = DefaultRouter()
router.register(r'post',PostViewSet,basename='api-post')
router.register(r'category',CategoryViewSet,basename='api-category')
router.register(r'tag',CategoryViewSet,basename='api-tag')



# class-based view
from blog.views import PostDetailView,IndexView,CategoryView,TagView,SearchView,AuthorView,PostAddView
from config.views import LinkListView

urlpatterns = [
    path('super_admin/', admin.site.urls),
    path('admin/', custom_site.urls),
    # path('',post_list,name='index'),
    path('',IndexView.as_view(),name='index'),
    # path('post/<int:post_id>',post_detail, name='post-detail'),
    path('post/<int:post_id>',PostDetailView.as_view(), name='post-detail'),
    # path('category/<int:category_id>',post_list,name='category-detail'),
    path('category/<int:category_id>',CategoryView.as_view(),name='category-detail'),
    # path('tag/<int:tag_id>',post_list, name='tag-detail'),
    path('tag/<int:tag_id>',TagView.as_view(), name='tag-detail'),

    path('search/',SearchView.as_view(), name='search'),

    path('author/<int:owner_id>', AuthorView.as_view(), name='author'),

    path('links/', LinkListView.as_view(), name='links'),

    path('comment/', CommentView.as_view(), name='comment'),

    path('ckeditor/',include('ckeditor_uploader.urls')),

    path('addpost/',PostAddView.as_view(), name='add-post'),
    # rest api
    # path('api/post',PostList.as_view(),name='post-list')
    path('api/',include((router.urls,'rest_framework'),namespace='api')),
    path('api/docs/',include_docs_urls(title='typediea apis')),

    path('login/',LoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
