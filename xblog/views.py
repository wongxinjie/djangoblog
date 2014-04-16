#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from xblog.models import Blog, Category, Tag, ClientInfo 
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime

def blog_list(request):
	blog_list = Blog.objects.all()
	
	paginator = Paginator(blog_list, 4)
	page = request.GET.get('page')
	
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)

	categories = Category.objects.all()
	tags = Tag.objects.all()
	try:
		real_ip = request.META['HTTP_X_FORWARDED_FOR']
        	regip = real_ip.split(",")[0]
	except:
		try:
			regip = request.META['REMOVE_ADDR']
		except:
			regip= ""
	client_info = ClientInfo()
	client_info.ip_address = regip

	return render_to_response("blog_list.html", {"blogs":blogs, "categories": categories, "tags": tags, "paginator": paginator })


def blog_show(request, article_id):
	try:
		blog = Blog.objects.get(article_id=article_id)
		categories = Category.objects.all()
		tags = Tag.objects.all()
	except blog.DoesNotExist:
		raise Http404
	return render_to_response("blog_show.html", {"blog":blog, "article_id":article_id,  "categories": categories, "tags": tags })


def category(request, slug):
	cut_category = get_object_or_404(Category, slug=slug)
        blogs = cut_category.blog_set.all()
	categories = Category.objects.all()
	tags = Tag.objects.all()
	return render_to_response("blog_list.html", {"blogs": blogs, "categories": categories, "tags": tags})

def tag(request, id=''):
	cut_tag = Tag.objects.get(id=id)
	blogs = cut_tag.blog_set.all()
	tags = Tag.objects.all()
	categories = Category.objects.all()
	return render_to_response("blog_list.html", {"blogs":blogs, "categories": categories, "tags": tags})

#add a function to search the blog.
def search_blog(request):
	query = request.GET.get('title', '')
	if query:
		query_set=(Q(caption__icontains = query))
		blogs = Blog.objects.filter(query_set).distinct()
	else:
		blogs = []
	
	tags = Tag.objects.all()
	categories = Category.objects.all()
		
	return render_to_response("blog_list.html", {"blogs":blogs,
"categories": categories, "tags": tags})


def about(request):
	return render_to_response("about.html", {})

def contact(request):
	return render_to_response("contact.html", {})





































