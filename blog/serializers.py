from rest_framework import serializers

from blog.models import Article, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("url", "name")


class ArticleHyperlinkedListSerializer(serializers.HyperlinkedModelSerializer):
    """
        API V1
        GET, POST
    """
    time_to_read = serializers.CharField(max_length=5, read_only=True)
    content = serializers.CharField(write_only=True)
    category = serializers.CharField(max_length=60)

    class Meta:
        model = Article
        fields = ('url', 'title', 'content', 'time_to_read', 'category', 'created')


class ArticleHyperlinkedRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    """
        API V1
        RETRIEVE, PUT, DELETE, PATCH
    """
    time_to_read = serializers.CharField(max_length=5, read_only=True)
    category = serializers.CharField(max_length=60)

    class Meta:
        model = Article
        fields = ('url', 'title', 'content', 'time_to_read', 'category', 'modified', 'created')


class ArticleModelListSerializer(serializers.ModelSerializer):
    """
        API V2
        GET, POST
    """
    time_to_read = serializers.CharField(max_length=5, read_only=True)
    category = serializers.CharField(max_length=60)
    content = serializers.CharField(write_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'time_to_read', 'category', 'created')


class ArticleModelRetrieveSerializer(serializers.ModelSerializer):
    """
        API V2
        RETRIEVE, PUT, DELETE, PATCH
    """
    time_to_read = serializers.CharField(max_length=5, read_only=True)
    category = serializers.CharField(max_length=60)

    class Meta:
        model = Article
        fields = ('title', 'content', 'time_to_read', 'category', 'modified', 'created')


class ArticleListSerializer(serializers.Serializer):
    """
        API V3
        GET, POST
    """
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=60)
    time_to_read = serializers.CharField(max_length=5, read_only=True)
    category = serializers.CharField(max_length=60)
    content = serializers.CharField(write_only=True)
    created = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return Article(**validated_data)


class ArticleRetrieveSerializer(serializers.Serializer):
    """
        API V3
        RETRIEVE, PUT, DELETE, PATCH
    """
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=60)
    time_to_read = serializers.CharField(max_length=5, read_only=True)
    category = serializers.CharField(max_length=60)
    content = serializers.CharField()
    created = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.category = validated_data.get('category', instance.category)
        return instance
    
    

