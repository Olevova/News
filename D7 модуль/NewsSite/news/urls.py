from django.urls import path
from .views import *
from allauth.account.views import LogoutView, LoginView

urlpatterns = [
                path('', NewsList.as_view(), name = 'allnews'),
                path('<int:pk>', News.as_view(), name="ObjNews.html"),
                path('add/', NewsCreateView.as_view(), name='add'),
                path('<int:pk>/edit', NewsUpd.as_view(), name='add'),
                path('delete/<int:pk>', NewsDel.as_view(), name='news_del'),
                path('upgrade/', upgrade_me, name='upgrade'),
                path('cat/<int:pk>', NewsCat.as_view(), name = 'cat'),
                path('subscribe/<int:pk>',Sub_Cut, name='sub')
                ]
