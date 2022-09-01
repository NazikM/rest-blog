from django.contrib import admin
from django.urls import path, include

from blog.views import CategoryViewSet, ArticleViewSet, ArticleListCreateAPIView, ArticleRetrieveUpdateDeleteAPIView, \
    ArticleAPIView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'article', ArticleViewSet, basename='article')


urlpatterns = [
    path('admin/', admin.site.urls),

    # API V1
    path('api/v1/', include(router.urls)),

    # API V2
    path('api/v2/', ArticleListCreateAPIView.as_view()),
    path('api/v2/<int:pk>', ArticleRetrieveUpdateDeleteAPIView.as_view()),

    # API V3

    path('api/v3/', ArticleAPIView.as_view()),
    path('api/v3/<int:pk>', ArticleAPIView.as_view()),
]
