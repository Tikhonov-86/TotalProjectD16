from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from testapp.models import Comment


@shared_task
def comment_created_task(comment_id, email, subject):
    comment = Comment.objects.get(pk=comment_id)
    email = comment.add.author.user.email

    subejct = f'На Ваше объявление оставили отклик'

    text_content = (
        f'Объявление: {instance.title}\n'
        f'Описание: {instance.text}\n\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Объявление: {instance.title}<br>'
        f'Описание: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1/{instance.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )

    msg = EmailMultiAlternatives(subject, text_content, skillfactory@mail.ru, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()