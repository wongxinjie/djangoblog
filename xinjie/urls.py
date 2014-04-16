#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from xblog.views import *

from django.contrib import admin
admin.autodiscover()
import xblog.admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xinjie.views.home', name='home'),
    # url(r'^xinjie/', include('xinjie.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$', 'xblog.views.blog_list', name='blog_list'),
     url(r'^bloglist/$', 'xblog.views.blog_list', name='blog_list'), 
     url(r'^article/(?P<article_id>(\d+))/$', 'xblog.views.blog_show', name='blog_article'),
     url(r'^searchblog/', 'xblog.views.search_blog', name= 'search_blog'),
     

     url(r'^category/(?P<slug>[-\w]+)/$', 'xblog.views.category', name='blog_category'),
     url(r'^tag/(?P<id>(\d+))/$', 'xblog.views.tag', name='blog_tag'),
     
     url(r'^about/$', 'xblog.views.about'),
     url(r'^contact/$', 'xblog.views.contact'),
)

