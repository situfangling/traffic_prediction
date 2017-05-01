from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from process.views import *

urlpatterns = patterns('process.views',
 url(r'^index$','index',name='index'),
)