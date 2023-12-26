from django.urls import path

from .views import ArticleList, ArticleDetail, ArticleUpdate


urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
]
