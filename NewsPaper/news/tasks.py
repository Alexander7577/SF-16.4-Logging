import datetime

from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import render_to_string
from django.utils import timezone
from celery import shared_task
from .models import Post, Category


@shared_task
def send_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    subscribers = []
    for category in categories:
        subscribers += category.subscribers.all()
    subscribers = set(subscribers)
    for subscriber in subscribers:
        html_content = render_to_string(
            'account/email/post_created_email.html',
            {
                'text': f'{post.content[:100]}...',
                'link': f"http://127.0.0.1:8000/news/{pk}"
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{post.title}',
            body='',
            from_email='Chudalex1999@yandex.ru',
            to=[subscriber.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_delete_notification(title):
    mail_managers(
        subject=f'Удаление поста',
        message=f'пост {title} был удалён!',
    )


@shared_task
def weekly_notification():
    today = timezone.now().date()
    last_week = today - datetime.timedelta(weeks=1)
    posts = Post.objects.filter(date_time__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subscribers = Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True)
    html_content = render_to_string(
        'account/email/daily_post.html',
        {
            'posts': posts
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи вышедшие за эту неделю!',
        body='',
        from_email='Chudalex1999@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()




