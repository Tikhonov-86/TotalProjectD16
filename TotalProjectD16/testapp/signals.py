from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail, EmailMultiAlternatives

from .models import Article


# @receiver(pre_save, sender=UserResponse)
# def my_handler(sender, instance, created, **kwargs):
#     if instance.status:
#         mail = instance.author.email
#         send_mail(
#             'Subject here',
#             'Here is the message.',
#             'skillfactorytest@yandex.ru',
#             [mail],
#             fail_silently=False
#         )
#     mail = instance.article.author.email
#     send_mail(
#         'Subject here',
#         'Here is the message.',
#         'skillfactorytest@yandex.ru',
#         [mail],
#         fail_silently=False
#     )


# @receiver(post_save, sender=Article)
# def product_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = Article.objects.filter(
#         subscriptions__category=instance.TYPE
#     ).values_list('email', flat=True)
#
#     subject = f'Новое объявление в категории {instance.TYPE}'
#
#     text_content = (
#         f'Объявление: {instance.title}\n'
#         f'Описание: {instance.text}\n\n'
#         f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Объявление: {instance.title}<br>'
#         f'Описание: {instance.text}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на объявление</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#
#
# @receiver(post_save, sender=Article)
# def product_created(instance, **kwargs):
#     print('Создано объявление', instance)
