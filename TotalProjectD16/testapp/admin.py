from django.contrib import admin
from django import forms
from testapp.models import Article, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(forms.ModelAdmin):
    form = ArticleAdminForm


admin.site.register(Article, ArticleAdmin)
admin.site.register(User)
