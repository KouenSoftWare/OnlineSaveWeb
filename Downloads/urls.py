#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url

from . import views

app_name = 'Downloads'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^table', views.table, name='table'),
    url(r'^downFile', views.downFile, name='downFile'),
]