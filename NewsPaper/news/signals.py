from django.db.models.signals import post_save, post_delete, m2m_changed, pre_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import send_mail, mail_managers, EmailMultiAlternatives
from .models import Post, PostCategory, User
from django.template.loader import render_to_string
from django.core import serializers
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

from .tasks import send_new_post, send_delete_notification


# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         send_new_post.delay(instance.pk)


@receiver(post_delete, sender=Post)
def notify_about_delete_post(sender, instance, **kwargs):
    send_delete_notification.delay(instance.title)


@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    if instance.pk is None:
        # Новый пост, выполняем проверку
        today = timezone.now().date()
        start_time = datetime.datetime.combine(today, datetime.time.min)
        end_time = datetime.datetime.combine(today, datetime.time.max)

        post_count = Post.objects.filter(author=instance.author, date_time__range=(start_time, end_time)).count()

        if post_count >= 3:
            raise ValidationError("Превышено ограничение на количество постов в сутки.")


@receiver(user_signed_up)
def welcome_email(sender, **kwargs):
    user = kwargs['user']
    if user.is_active:
        html_content = render_to_string(
            'account/email/welcome_email.html',
            {
                'text': f'{user.username}, мы очень рады, что ты теперь с нами на нашем новостном портале!',
            }
        )
        msg = EmailMultiAlternatives(
            subject='Добро пожаловать!',
            body='',
            from_email='Chudalex1999@yandex.ru',
            to=[user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()