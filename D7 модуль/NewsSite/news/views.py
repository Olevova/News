from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import *
from django.views.generic import ListView, DetailView,CreateView,DeleteView, UpdateView
from .filters import PostFilter
from .form import NewsForm
from django.contrib.auth.models import Group
from django.core.mail import mail_admins,EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from news.tasks import *

class NewsList(ListView):#вывод списка новостей
    model = Post
    template_name = "news.html"
    context_object_name = 'news'
    queryset = Post.objects.order_by('-create')#сортировка новостей по добавлению
    paginate_by = 4 # пагинация с выводом 4 новостей

    def get_filter(self):
        #print(super().get_queryset())
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        #print(self.get_filter().qs)
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                'filter': self.get_filter,
                'category': Category.objects.all(),
                #'NC': Category.objects.get(post__pk = self.pk)
                }

class NewsCat(ListView): # вывод категорий
    model = Post
    template_name = "news.html"
    context_object_name ='news'
    paginate_by = 4

    def get_queryset(self):
        print(Post.objects.filter(category__pk=self.kwargs['pk']))
        print(self.kwargs['pk'])
        return Post.objects.filter(category__pk=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['category_selected'] = self.kwargs['pk']
        context['not_sub'] = self.cat_sub()
        print(self.cat_sub(), context['category_selected'])
        return context

    def cat_sub(self):
        print(self.request.user)
        cat = Category.objects.get(pk=self.kwargs['pk'])
        sub = SubAuthor.objects.filter(subcat=cat)
        g = []
        if str(self.request.user) == 'AnonymousUser':
            False
        else:
            for r in sub:
                g.append(r.subaut)
            print(g)
            print(self.request.user.author)
            if not self.request.user.author in g:
                print('ok')
                return True
            else:
                print('no')
                False


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_Post')
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #printer.apply_async([10],eta = datetime.now() + timedelta(seconds=5))
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


   #def post(self, request, *args, **kwargs): # один из способов рассылки с помощью функции. Сделан для категории Спорт
   #        title = request.POST['title']
   #        content = request.POST['content']
   #        text = request.POST['text']
   #        author = Author.objects.get(pk = request.POST['author'])
   #        category = Category.objects.get(pk = request.POST['category'])
   #        #print(category, text, author)
   #        html_content = render_to_string(
   #            'OneNewsCreated.html',
   #            {
   #                'title': title, 'content': content, 'text': text, 'author': author, 'category':category,
   #            }
   #        )
   #        mails = []
   #        #if str(category) == 'Sport1':
   #            #print('ok')
   #        r = SubAuthor.objects.filter(subcat__name=category)
   #        for i in r:
   #            if len(i.subaut.user.email)>1:
   #                mails.append(str(i.subaut.user.email))

   #        print(mails)
   #        msg = EmailMultiAlternatives(
   #            subject=f'{title} {category}',
   #            body = text ,
   #            from_email='olevova1983@gmail.com',
   #            to = mails,
   #        )
   #        msg.attach_alternative(html_content, "text/html")  # добавляем html

   #        msg.send()  # отсылаем

   #        return super().post(request, *args, **kwargs)


class News(DetailView):#вывод для одной новости
    model = Post
    template_name = 'ObjNews.html'
    context_object_name = 'piece'
    queryset = Post.objects.all()


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timenow'] = datetime.now()
        context['auf'] = Author.objects.all()
        return context


class NewsDel(LoginRequiredMixin , DeleteView):
    login_url = '/'
    template_name = 'news_del.html'
    context_object_name = "piece"
    queryset = Post.objects.all()
    success_url = '/'

class NewsUpd(LoginRequiredMixin,UpdateView):
    login_url = '/'
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = '/'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        #printer.delay(5)
        return Post.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        print(context)
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='subaut')
    if not request.user.groups.filter(name='subaut').exists():
        authors_group.user_set.add(user)
    return redirect('/')


@login_required #
def Sub_Cut(request,**kwargs):
    cat_number = int(kwargs['pk'])
    cat = Category.objects.get(pk=cat_number)
    print(cat)
    sub = SubAuthor.objects.filter(subcat=cat)
    g = []
    for r in sub:
        g.append(r.subcat)
    print(g)
    if not request.user.author in g:
        SubAuthor.objects.create(subaut=request.user.author, subcat=cat)
    return redirect('/')