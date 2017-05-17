from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from process.views import *

urlpatterns = patterns('process.views',
 url(r'^index$','index',name='index'),
 url(r'^data_preprocess$','data_preprocess',name='data_preprocess'),
 url(r'^query_status$','query_status',name='query_status'),
)