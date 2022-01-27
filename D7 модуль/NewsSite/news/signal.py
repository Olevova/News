from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_admins, mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Category, Post, PostCategory, SubAuthor


@receiver(post_save, sender = Category)

def SendNewCat(sender, instance, created, **kwargs):
    if created:
        subjects = f'Создана категория {instance.name}'
    else:
        subjects = f'Изменина категория {instance.name}'
    mail_admins(
        subject=subjects,
        message=f'Create category',
    )
    print(subjects)

@receiver(post_delete, sender = Post)
def SendDelPost(sender, instance, **kwargs):
    subjects = f'Новость {instance.title} удалена'
    mail_managers(
        subject=subjects,
        message=f'DEl News',
    )
    print(subjects)

@receiver(m2m_changed, sender = Post.category.through) # Рассылка подписчикам новых статей по категории
def SendNewCat(sender, instance, **kwargs):
    r = instance.category.all()
    print(r)
    subjects = f'Новость {instance.title} создана'
    cat = ''
    for i in r:
        cat = i
    print(cat)
    c = SubAuthor.objects.filter(subcat__name=cat)
    mails = []
    for i in c:
        if len(i.subaut.user.email) > 1:
            mails.append(str(i.subaut.user.email))
    html_content = render_to_string(
        'OneNewsCreated.html',
        {
            'title': instance.title,
            'content': instance.content,
            'text': instance.text,
            'author': instance.author,
            'category': instance.category,
            "link": instance.pk, # добавим в шаблон для создания ссылки на новость
        }
    )
    msg = EmailMultiAlternatives(
        subject= subjects,
        body=f'{instance.text[:15]}',
        from_email='olevova1983@gmail.com',
        to=mails,
        )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print(subjects, print())