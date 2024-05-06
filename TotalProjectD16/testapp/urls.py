from django.urls import path

from .views import (
    ArticleList, ArticleCreate, ArticleDetail, ArticleUpdate, ArticleDelete,
    IndexView, CommentCreate, CommentUpdate, CommentDelete, ConfirmUser, confirm_comment, reject_comment,
)

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('profile/', IndexView.as_view(), name='profile'),
    path('<int:pk>/comment/create/', CommentCreate.as_view(), name='comment_create'),
    path('<int:pk>/comment/update/', CommentUpdate.as_view(), name='comment_update'),
    path('<int:pk>/comment/delete/', CommentDelete.as_view(), name='comment_delete'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('int:pk>/comment/confirm/', confirm_comment, name='confirm_comment'),  # принять отклик
    path('int:pk>/comment/reject/', reject_comment, name='reject_comment'),  # отклонить отклик
]
