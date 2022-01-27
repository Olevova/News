import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','NewsSite.settings')
app = Celery('NewsSite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#рассылка новостей еженедельно(период неделя)
app.conf.beat_schedule = {
    'every_week_news_mailing_list': {
        'task': 'news.tasks.SendNew',
        #'schedule': crontab(),
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
