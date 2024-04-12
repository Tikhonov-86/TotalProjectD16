from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from TotalProjectD16 import settings
from testapp.models import Comment


@shared_task
def comment_created_task(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    email = comment.add.author.user.email

    subject = f'На Ваше объявление оставили отклик'

    text_content = (
        f'Объявление: {comment.commentPost}\n'
        f'Описание: {comment.text}\n\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{comment.get_absolute_url()}'
    )
    html_content = (
        f'Объявление: {comment.commentPost}<br>'
        f'Описание: {comment.text}<br><br>'
        f'<a href="http://127.0.0.1/{comment.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def confirm_comment_task(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    email = comment.user.email

    if comment.status == 'accepted':
        subject = f'Ваш отклик приняли'

        text_content = (
            f'Объявление: {comment.commentPost}\n'
            f'Описание: {comment.text}\n\n'
            f'Ссылка на объявление: http://127.0.0.1:8000{comment.get_absolute_url()}'
            f'Принят автором объявления: {comment.add.author.user}'
        )
        html_content = (
            f'Объявление: {comment.commentPost}<br>'
            f'Описание: {comment.text}<br><br>'
            f'<a href="http://127.0.0.1/{comment.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
            f'Принят автором объявления: {comment.add.author.user}'
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    elif comment.status == 'rejected':
        subject = f'Ваш отклик отклонили'
        text_content = (
            f'Объявление: {comment.commentPost}\n'
            f'Описание: {comment.text}\n\n'
            f'Ссылка на объявление: http://127.0.0.1:8000{comment.get_absolute_url()}'
            f'Отклонён автором объявления: {comment.add.author.user}'
        )
        html_content = (
            f'Объявление: {comment.commentPost}<br>'
            f'Описание: {comment.text}<br><br>'
            f'<a href="http://127.0.0.1/{comment.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
            f'Отклонён автором объявления: {comment.add.author.user}'
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()