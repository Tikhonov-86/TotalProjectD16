import random
from string import hexdigits

from django import forms
from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.forms import TextInput, Textarea
from django.conf import settings
from allauth.account.forms import SignupForm

from .models import Article, Comment


class CommonSingupForm(SignupForm):
    def save(self, request):
        user = super(CommonSingupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.mail],
        )
        return user


class ArticleForm(forms.ModelForm):
    text = forms.Textarea(min_length=15)

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

    class Meta:
        model = Article
        fields = ['title', 'text', 'category', 'author']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок объявления'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание объявления'}),
            'category_': TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'}),
            'author_': TextInput(attrs={'class': 'form-control', 'placeholder': 'Автор'}),
        }


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
