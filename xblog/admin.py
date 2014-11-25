#-*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from models import Category, Tag, Blog, Picture,  BlogPicture, ClientInfo, Document

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']
	prepopulated_fields = {'slug': ('name', )}

class PictureAdmin(admin.ModelAdmin):
	list_display = ['title', 'image', 'thumb', 'upload_date']
	ordering = ['-upload_date']


class BlogAdmin(admin.ModelAdmin):
	list_display = ['caption', 'article_id', 'id',  'counts', 'category', 'published_time']
	list_filter = ['caption']
	prepopulated_fields = {'article_id': ('caption', )}
	ordering = ['-published_time']
	filter_horizontal = ('tags', 'blog_pictures',)


class ClientInfoAdmin(admin.ModelAdmin):
	list_display = ['ip_address', 'time']
	ordering = ('time', )

class DocumentAdmin(admin.ModelAdmin):
	list_display = ['title', 'url']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Picture, PictureAdmin)
admin.site.register(BlogPicture)
admin.site.register(ClientInfo, ClientInfoAdmin)
admin.site.register(Document, DocumentAdmin)
