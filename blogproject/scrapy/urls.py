"""HZLCMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path
from scrapy import views as scrapy_views

app_name = 'scrapy'

urlpatterns = [
    path('category', scrapy_views.category_request, name='category_request'),
    path('chapter', scrapy_views.chapter_request, name='chapter_request'),
    path('info', scrapy_views.info_request, name='info_request'),
    path('content', scrapy_views.content_request, name='content_request'),
    path('search', scrapy_views.search_request, name='search_request'),
    path('source', scrapy_views.source_request, name='source_request'),
    path('test', scrapy_views.test_request, name='test_request'),
]
