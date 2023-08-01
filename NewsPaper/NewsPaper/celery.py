import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'weekly_notification': {
        'task': 'news.tasks.weekly_notification',
        'schedule': crontab(day_of_week='monday', hour='8', minute='0'),
    },
}
