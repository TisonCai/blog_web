from rest_framework import serializers,pagination

from django.contrib.auth.models import User
from .models import SideBar
from blog.models import Post
from comment.models import Comment  # 防止循环引用
from blog.serializers import PostSerializer
from comment.serializers import CommentSerializer
from login.serializers import UserSerializer


class SideBarSerializer(serializers.ModelSerializer):
    side_list = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self,obj):
        request = self.context['request']
        display_type = obj.display_type
        list = None

        if display_type == SideBar.DISPLAY_HTML:
            return None
        elif display_type == SideBar.DISPLAY_LATEST:
            post = Post.lastes_posts()
            serializer = PostSerializer(post, many=True, context={'request': request})
            list = serializer.data
        elif display_type == SideBar.DISPLAY_HOT:
            post = Post.hot_posts()
            serializer = PostSerializer(post, many=True, context={'request': request})
            list = serializer.data
        elif display_type == SideBar.DISPLAY_COMMENT:
            comment = Comment.objects.filter(status=Comment.STATUS_NORMAL)
            serializer = CommentSerializer(comment, many=True, context={'request': request})
            list = serializer.data
        elif display_type == SideBar.DISPLAY_Author:
            if request.user is None:
                list = []
            else:
                serializer = UserSerializer(request.user,)
                list = [serializer.data]
        return list
        # return {
        #     'type' : display_type,
        #     'sides' : list,
        # }

    class Meta:
        model = SideBar
        fields = ['id', 'title', 'display_type','side_list']

