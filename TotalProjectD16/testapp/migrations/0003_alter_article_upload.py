# Generated by Django 5.0 on 2024-05-24 07:04

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_alter_article_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='upload',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Загрузка файла'),
        ),
    ]
