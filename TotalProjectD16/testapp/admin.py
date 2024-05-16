from django.contrib import admin
from django.contrib.gis import forms

from testapp.models import Article, User

from ckeditor_uploader.widgets import CKEditorUploadingWidget


admin.site.register(Article)
admin.site.register(User)


class ArticleAdminForm(forms.ModelForm):
    text = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'
