from rest_framework import serializers,pagination

from .models import Post,Category,Tag

class PostSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    def create(self, validated_data):
        return super(PostSerializer, self).create(self,validated_data)

    class Meta:
        model = Post
        fields = ['id','title','category','tag','owner','create_time']
        # extra_kwargs = {
        #     'url': {'view_name': 'api-post-detail'}
        # }


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id','title','category','tag','owner','create_time','content_html']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'create_time', ]


class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self,obj):
        request = self.context['request']
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)

        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts,request)
        print('=============page============')
        print(page)
        print(posts)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return {
            'count': posts.count(),
            'post_list': serializer.data,
            # 'previous': paginator.get_previous_link(),
            # 'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = ['id', 'name', 'create_time', 'posts']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'create_time',]


class TagDetailSerializer(TagSerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        request = self.context['request']
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return {
            'count': posts.count(),
            'post_list': serializer.data,
        }
    class Meta:
        model = Tag
        fields = ['id', 'name', 'create_time','post']