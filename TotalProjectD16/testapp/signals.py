from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail

from .models import UserResponse


@receiver(pre_save, sender=UserResponse)
def my_handler(sender, instance, created, **kwargs):
    mail = instance.article.author.email
    send_mail(
        'Subject here',
        'Here is the message.',
        'skillfactorytest@yandex.ru',
        [mail],
        fail_silently=False
    )

