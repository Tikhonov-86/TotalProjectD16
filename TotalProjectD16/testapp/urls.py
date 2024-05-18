from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    ArticleList, ArticleCreate, ArticleDetail, ArticleUpdate, ArticleDelete,
    IndexView, CommentCreate, CommentUpdate, CommentDelete, ConfirmUser, accept_rejected,
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
    path('<int:pk>/comment/confirm/', accept_rejected, name='confirm_comment'),  # принять отклик
    path('<int:pk>/comment/reject/', accept_rejected, name='reject_comment'),  # отклонить отклик
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset',),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done',),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm',),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',),
]
