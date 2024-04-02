import django_filters
from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter

from .models import *

# class ArticleFilter(FilterSet):
#     class Meta:
#         model = Article
#         fields = {
#             'author': ['icontains'],
#             'category': ['icontains'],
#             'dateCreation': ['icontains'],
#         }
#


class CommentFilter(FilterSet):
    model = Comment
    fields = {'commentPost', 'Article', 'dateCreation'}
    commentPost = django_filters.CharFilter(
        field_name='commentPost',
        lookup_expr='icontains',
        label='Комментарий',
    )
    search_category = ModelChoiceFilter(
        field_name='category',
        queryset=Article.objects.all(),
        label='Категория',
        empty_label='Все категории',
    )
    date = django_filters.IsoDateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата публикации',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )

