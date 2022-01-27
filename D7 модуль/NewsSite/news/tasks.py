from datetime import datetime, timedelta, timezone
from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category, SubAuthor


#shared_task
#ef printer():
#   for i in range(5):
#       time.sleep(1)
#       print(i+1)



@shared_task #рассылка новостей еженедельно(период неделя)
def SendNew():
    week_news = Post.objects.filter(create__range=[datetime.now(timezone.utc) - timedelta(days=7), datetime.now(timezone.utc)])
    print(week_news)
    for i in week_news:
        print(i.title, i.create)
    first_date = datetime.now(tz=timezone.utc)
    last_date = datetime.now(tz=timezone.utc) - timedelta(days=7)
    cat = Category.objects.all()
    print('ok',first_date, last_date)
    for item in cat:
        print(item)
        cat_post = Post.objects.filter(create__range=[datetime.now(timezone.utc) - timedelta(days=15), datetime.now(timezone.utc)], category=item)
        sub_cat = SubAuthor.objects.filter(subcat__name=item)
        mails = []
        for i in sub_cat:
            print(i.subaut.user.email)
            if len(i.subaut.user.email) > 1:
                mails.append(str(i.subaut.user.email))
        print(mails, item)
        html_content = render_to_string('newslist.html',{'newslist':cat_post})
        msg = EmailMultiAlternatives(
            subject=item,
            body='list',
            from_email='olevova1983@gmail.com',
            to=mails,)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

#"@shared_task
#def SendNew():
#    Nl = Post.objects.filter(create__gt = datetime.now() - timedelta(weeks=1))
#    Subs = Author.objects.filter()
#    mails = []
#    for i in Subs:
#        if len(i.user.email) > 1:
#            mails.append(str(i.user.email))
#    html_content = render_to_string(
#        'news.html',
#        {
#            'news': Nl,
#        }
#    )
#    msg = EmailMultiAlternatives(
#        subject='week news',
#        body='week news',
#        from_email = 'olevova1983@gmail.com',
#        to=mails,
#        )
#    msg.attach_alternative(html_content, "text/html")
#    msg.send()