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
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=16, choices=TYPE, default='tank', verbose_name='Категория')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    upload = models.FileField(
        upload_to='uploads/', help_text='Загрузите файл', blank=True, verbose_name='Загрузка файла'
    )

    def __str__(self):
        return f'{self.dateCreation}||{self.title}:{self.text[:20]}'

    def get_absolut_url(self):
        return f'/article/{self.id}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-dateCreation']


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Объявление')
    status = models.BooleanField(default=False, verbose_name='Статус')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['id']


class Comment(models.Model):
    commentPost = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Комментарии')
    commentUser = models.ForeignKey(UserResponse, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Описание')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.commentUser} : {self.text} [:20] + ...'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['id']


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


