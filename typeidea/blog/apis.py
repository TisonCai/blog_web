from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import viewsets

from django.db.models import Q,F
from .models import Post,Category,Tag
from .serializers import PostSerializer,PostDetailSerializer,CategorySerializer,CategoryDetailSerializer,\
    TagSerializer,TagDetailSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        user_id     = request.GET.get('user_id',-1)
        category_id = request.GET.get('category_id', -1)
        tag_id      = request.GET.get('tag_id', -1)
        keyword     = request.GET.get('keyword', "")
        posts = None
        print("{} {} {} keyword:{}".format(user_id, category_id, tag_id,keyword))

        if user_id is not None and user_id != -1:
            posts = Post.objects.filter(owner_id=user_id)
        elif category_id is not None and category_id != -1:
            posts = Post.objects.filter(category_id=category_id)
        elif tag_id is not None and tag_id != -1:
            posts = Post.objects.filter(tag_id=tag_id)
        elif keyword is not None:
            posts = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
        else:
            posts = Post.objects.filter(status=Post.STATUS_NORMAL)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = TagSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super().retrieve(request, *args, **kwargs)

