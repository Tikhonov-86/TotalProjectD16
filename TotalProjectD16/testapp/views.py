from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import OuterRef, Exists
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import ArticleForm
from .models import Article, Subscription


class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 5


class ArticleDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('testapp.add_article',)
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'


def create_news(request):
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/article/')

    return render(request, 'article_create.html', {'form': form})


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('testapp.add_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_create.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('testapp.update_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_update.html'
    success_url = reverse_lazy('article')

    # def form_valid(self, form):
    #     form.instance.author = self.request.user.author
    #     return super().form_valid(form)


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('testapp.delete_article',)
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article')


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

