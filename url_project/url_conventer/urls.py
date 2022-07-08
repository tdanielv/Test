from django import views
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include

from .views import index, convent, UrlsByUser, register

urlpatterns = [
    path('', index, name='main_page'),
    path('main_page/', index, name='main_page'),
    path('conventer/', convent, name='conventer'),
    path('myurls/', UrlsByUser.as_view(), name='my_urls'),
    path( 'register/', register, name='register'),
]
