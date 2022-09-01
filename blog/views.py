from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Article, Category
from blog.serializers import CategorySerializer, ArticleHyperlinkedListSerializer, ArticleHyperlinkedRetrieveSerializer, \
    ArticleModelListSerializer, ArticleModelRetrieveSerializer, ArticleListSerializer, ArticleRetrieveSerializer
from rest_framework.pagination import LimitOffsetPagination


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
         API V1 ( VIEWSET )
         GET, POST, RETRIEVE, PUT, DELETE, PATCH
    """
    queryset = Article.objects.all()
    serializer_class = ArticleHyperlinkedRetrieveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', ]
    search_fields = ['title', 'content']

    def list(self, request, *args, **kwargs):
        ArticleViewSet.serializer_class = ArticleHyperlinkedListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        ArticleViewSet.serializer_class = ArticleHyperlinkedRetrieveSerializer
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        ArticleViewSet.serializer_class = ArticleHyperlinkedRetrieveSerializer
        return super().update(request, *args, **kwargs)


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    """
        API V2 ( GENERIC )
        GET, POST
    """
    queryset = Article.objects.all()
    serializer_class = ArticleModelListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', ]
    search_fields = ['title', 'content']


class ArticleRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        API V2 ( GENERIC )
        RETRIEVE, PUT, DELETE, PATCH
    """
    queryset = Article.objects.all()
    serializer_class = ArticleModelRetrieveSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleAPIView(APIView):
    """
        API V3 ( APIVIEW )
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', ]
    search_fields = ['title', 'content']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            filter_backend = backend()
            setattr(filter_backend, 'filterset_fields', self.filterset_fields)
            setattr(filter_backend, 'search_fields', self.search_fields)
            queryset = filter_backend.filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request, pk=None):
        if not pk:
            articles = Article.objects.all()

            # Filter
            filtered_qs = self.filter_queryset(queryset=articles)

            # Pagination
            paginator = StandardResultsSetPagination()
            result_page = paginator.paginate_queryset(queryset=filtered_qs, request=request)

            serializer = ArticleListSerializer(result_page, many=True)
            return Response(serializer.data)
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleRetrieveSerializer(article)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleRetrieveSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)