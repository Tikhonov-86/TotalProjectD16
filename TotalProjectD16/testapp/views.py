from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import OuterRef, Exists
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django_filters import FilterSet
from requests import Response

from .filters import CommentFilter
from .forms import ArticleForm, CommentForm
from .models import Article, Subscription, Comment, User


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
        return redirect('account_login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class ArticleFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ['commentPost']

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)
        self.filters['commentPost'].queryset = Article.objects.filter(author__id=kwargs['request'])


class IndexView(LoginRequiredMixin, ListView):
    form_class = CommentFilter
    model = Comment
    template_name = 'main.html'
    context_object_name = 'comments'
    # success_url = reverse_lazy('profile')

    def get_queryset(self):
        queryset = Comment.objects.filter(commentPost__author__id=self.request.user.id)
        self.filterset = ArticleFilter(self.request.GET, queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 10


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'article_detail.html'
    form_class = CommentForm
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commentUser = self.request.user
        comment.commentPost_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_id'] = self.kwargs['pk']
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('testapp.update_comment',)
    raise_exception = True
    form_class = CommentForm
    model = Comment
    template_name = 'comment_update.html'
    success_url = reverse_lazy('article_list')


class CommentDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('testapp.delete_comment',)
    raise_exception = True
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('article_list')


class ArticleDetail(DetailView, CommentCreate):
    permission_required = ('testapp.add_article',)
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'


class ArticleCreate(CreateView):
    permission_required = ('testapp.add_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_create.html'
    success_url = reverse_lazy('article_list')


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('testapp.update_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_update.html'
    success_url = reverse_lazy('article_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('testapp.delete_article',)
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


# def usual_login_view(self, request, *args, **kwargs):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return Response(
#             {"message": "Успешный вход в систему."},
#             status=status.HTTP_200_0K
#         )
#     else:
#         return Response(
#         {"error": "Неверные учетные данные."},
#         status=status.HTTP_401_UNAUTHORIZED
#         )


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Article.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Article.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


# class CategoryListView(ListView):
#     model = Article
#     template_name = 'category_list.html'
#     context_object_name = 'TYPE_Article'
#
#
#     def get_queryset(self):
#         self.category = get_object_or_404(Article, id=self.kwargs['pk'])
#         queryset = Article.objects.filter(category=self.category).order_by('-dateCreation')
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_subscriber'] = Subscription.objects.filter(user=self.request.user, category=self.category).exists()
#         context['category'] = self.category
#         return context
