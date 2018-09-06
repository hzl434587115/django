"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from . import views as blog_views
from .feeds import AllPostsRssFeed

app_name = 'blog'
urlpatterns = [
    path('index/', blog_views.index, name='index'),
    path('share/', blog_views.share, name='share'),
    path('blogList/<int:page>/', blog_views.blogList, name='blogList'),
    path('blog/<int:blog_id>/', blog_views.blogdetails, name='blogdetails'),
    path('user/<int:user_id>/', blog_views.user, name='user'),
    path('about/', blog_views.about, name='about'),
    re_path(r'^test/(?P<year>\d+)?$', blog_views.test), # 可选参数
    path('rss/', AllPostsRssFeed(), name='rss'), # rss订阅
    path('loginView/', blog_views.loginView, name='loginView'),
    path('login/', blog_views.login, name='login'),
    path('logout/', blog_views.logout, name='logout'),
    path('comment/', blog_views.comment, name='comment'),
]
