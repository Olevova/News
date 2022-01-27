from django.utils import timezone
from datetime import datetime, timedelta
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category, SubAuthor, Author

logger = logging.getLogger(__name__)


# задача отправки почты
def my_job():
    c1 = Post.objects.filter(create__range=[datetime.now(timezone.utc) - timedelta(days=7), datetime.now(timezone.utc)])
    print(c1)
    for i in c1:
        print(i.title, i.create)
    first_date = datetime.now(tz=timezone.utc)
    last_date = datetime.now(tz=timezone.utc) - timedelta(days=7)
    cat = Category.objects.all()
    print('ok',first_date, last_date)
    for item in cat:
        print(item)
        c = Post.objects.filter(create__range=[datetime.now(timezone.utc) - timedelta(days=15), datetime.now(timezone.utc)], category=item)
        p = SubAuthor.objects.filter(subcat__name=item)
        mails = []
        print(c,p)
        for i in p:
            print(i.subaut.user.email)
            if len(i.subaut.user.email) > 1:
                mails.append(str(i.subaut.user.email))
        print(mails, item)
        html_content = render_to_string('newslist.html',{'newslist':c})
        msg = EmailMultiAlternatives(
            subject=item,
            body='list',
            from_email='olevova1983@gmail.com',
            to=mails,)
        msg.attach_alternative(html_content, "text/html")
        msg.send()



# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="09", minute="00"),
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")


        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")