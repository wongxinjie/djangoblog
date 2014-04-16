#-*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from models import Category, Tag, Blog, Picture, ClientInfo

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']
	prepopulated_fields = {'slug': ('name', )}


class BlogAdmin(admin.ModelAdmin):
	list_display = ['caption', 'article_id', 'id',  'counts', 'category', 'published_time']
	list_filter = ['caption']
	prepopulated_fields = {'article_id': ('caption', )}
	ordering = ['-published_time']
	filter_horizontal = ('tags', 'blog_pictures',)


class ClientInfoAdmin(admin.ModelAdmin):
	list_display = ['ip_address', 'time']
	ordering = ('time', )

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(ClientInfo, ClientInfoAdmin)
