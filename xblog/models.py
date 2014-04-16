#-*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.db.models import permalink
from markdown import markdown


class Category(models.Model):
	name = models.CharField(max_length=20, verbose_name=u'名称')
	slug = models.CharField(max_length=30, verbose_name="slug")
	def __unicode__(self):
		return self.name
	
	@permalink
	def get_absolute_url(self):
		return ('blog_category', None, {'slug': self.slug})

	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'分类'


class Tag(models.Model):
	tag_name = models.CharField(max_length=20, blank=True, verbose_name = u'名称')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

	def __unicode__(self):
		return self.tag_name

	class Meta:
		verbose_name_plural = verbose_name = u'标签'

		

class Blog(models.Model):
	caption = models.CharField(max_length=50, verbose_name=u'标题')
        article_id  = models.IntegerField(unique=True, verbose_name=u'article_id')
	category = models.ForeignKey(Category, verbose_name=u'分类')
	tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签')
	counts = models.IntegerField(default=0, verbose_name=u' 阅读人数')
	content = models.TextField(verbose_name=u'内容')
	published_time = models.DateTimeField(auto_now=True, verbose_name=u'发表时间')
	updated_time = models.DateTimeField(auto_now = True, verbose_name=u'修改时间')

	def __unicode__(self):
		return u'%s %s' % ( self.caption, self.published_time)
        

	@permalink
	def get_absolute_url(self):
		return ('blog_article', None, {'article_id': self.article_id})

	
	class Meta:
		get_latest_by = 'published_time'
		ordering = ['-id']
		verbose_name_plural = verbose_name = u'文章'


class ClientInfo(models.Model):
	ip_address = models.CharField(max_length=30, verbose_name=u'访客IP')
	time = models.DateTimeField(auto_now=True, verbose_name=u'访问时间')

	def __unicode__self(self):
		return u'%s %s' % (self.ip_address, self.time)

	class Meta:
		get_latest_by = 'time'
		ordering = ['-id']
		verbose_name_plural = verbose_name = u'访问时间'



























