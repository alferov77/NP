"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from news.views import (
    NewsListView, NewsDetailView, search_news, PostCreateView, PostUpdateView, PostDeleteView,
    subscriptions
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('news/', cache_page(60 * 1)(NewsListView.as_view()), name='news_list'), # Кэширование на 1 минуту для главной страницы
    path('news/<int:pk>/', cache_page(60 * 5)(NewsDetailView.as_view()), name='news_detail'), # Кэширование на 5 минут для страницы деталей новости
    path('news/search/', search_news, name='search_news'),
    path('news/create/', PostCreateView.as_view(), name='post_create_news'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('articles/create/', PostCreateView.as_view(), name='post_create_article'),
    path('articles/<int:pk>/edit/', PostUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
