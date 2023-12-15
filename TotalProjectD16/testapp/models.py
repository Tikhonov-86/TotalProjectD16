from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    TYPE = (
        ('tank', 'Танк'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildmaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.OneToOneField(User, on_delete=models.CASCADE),
    title = models.CharField(max_length=64),
    text = models.TextField()
    category = models.CharField(max_length=16, choices=TYPE, default='tank')
    upload = models.FileField(upload_to='uploads/')


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE),
    title = models.CharField(max_length=64),
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


# class NewUser(User):
#     status = models.BooleanField(default=False)
#     auth_code = models.CharField(max_length=128, )