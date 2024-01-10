from django import forms
from django.core.exceptions import ValidationError

from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Article
        fields = [
            'title',
            'text',
            'author',
            'category',
        ]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы"
            )
        return title

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text[0].islower():
            raise ValidationError(
                "Описание должно начинаться с заглавной буквы"
            )
        return text


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Введите текст отклика:'
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 150, 'rows': 1}),
        }
