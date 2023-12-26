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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.CharField(max_length=16, choices=TYPE, default='tank')
    dateCreation = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='uploads/', help_text='Загрузите файл', blank=True)
    
    class Meta:
        ordering = ['-dateCreation']

    def __str__(self):
        return f'{self.dateCreation}||{self.title}:{self.text[:20]}'

    def get_absolut_url(self):
        return f'/forum/{self.id}'


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class Comment(models.Model):
    commentPost = models.ForeignKey(Article, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(UserResponse, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=UserResponse,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    article = models.ForeignKey(
        to='Article',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


