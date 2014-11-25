#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from xblog.models import Blog, Category, Tag, ClientInfo, Picture, BlogPicture, Document
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import BlogForm

import time
import datetime

def blog_list(request):
	blog_list = Blog.objects.all()
	
	paginator = Paginator(blog_list, 5)
	page = request.GET.get('page')
	
	try:
		blogs = paginator.page(page)
	except PageNotAnInteger:
		blogs = paginator.page(1)
	except EmptyPage:
		blogs = paginator.page(paginator.num_pages)

	categories = Category.objects.all()
	tags = Tag.objects.all()

	if request.META.has_key('HTTP_X_FORWARDED_FOR'):
		ip = request.META['HTTP_X_FORWARDED_FOR']
	else:
		ip = request.META['REMOTE_ADDR']
	
	if 'ip_address' not in request.session:
		request.session['ip_address'] = ip
		t = time.strftime("%Y-%m-%d %X", time.localtime(time.time()))
		client_info = ClientInfo(ip_address=ip, time = t)
		client_info.save()

	return render_to_response("blog_list.html", {"blogs":blogs, "categories": categories, "tags": tags, "paginator": paginator })


def blog_show(request, article_id):
	try:
		blog = Blog.objects.get(article_id=article_id)
		categories = Category.objects.all()
		tags = Tag.objects.all()
		blog_pictures = BlogPicture.objects.all()
		
		if article_id not in request.session:
			request.session[article_id] = 'readed'
			blog.counts += 1
			blog.save()
		
	except blog.DoesNotExist:
		raise Http404
	return render_to_response("blog_show.html", {"blog":blog, "article_id":article_id,  "categories": categories, "tags": tags, "blog_pictures": blog_pictures })

@login_required
def blog_edit(request, article_id):
	try:
		blog = Blog.objects.get(article_id=article_id)
	except Blog.DoesNotExit:
		raise Http404
	return render_to_response("edit.html", {"blog": blog}, context_instance=RequestContext(request))

@login_required
def blog_new(request):
	return render_to_response("edit.html", {})

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

def document(request):
	documents = Document.objects.all()
	return render_to_response("document.html", {"documents": documents, })
	
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

#@csrf_protect
def login_view(request):
	if request.method == "POST":
		user = authenticate(username=request.POST['user'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			blogs = Blog.objects.all()
			return render_to_response("admin_blog.html", {"blogs":blogs})
		else:
			#return render_to_response("login.html", {}, context_instance=RequestContext(request))
			return HttpResponseRedirect("/login/")
	else:
		#return render_to_response('login.html', {}, context_instance=RequestContext(request))
		return HttpResponseRedirect("/login/")
def admin_login(request):
	return render_to_response('login.html', {}, context_instance=RequestContext(request))

@login_required
def logout_view(request):
	logout(request)
	return render_to_response("login.html", {})

@login_required
def admin_blogs_list(request):
	blogs = Blog.objects.all()
	return render_to_response("admin_blog.html", {"blogs": blogs})

@login_required
def edit(request):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		if form.is_valid():
			caption = form.clean_data['caption']
			article_id = form.clean_data['article_id']
			category = form.clean_data['category']
			content = form.clean_data['content']
				
			blog = Blog(caption=caption,
				    article_id=article_id,
				    category=category,
				    content=content)
			blog.save()
			return HttpResponseRedirect("/bloglist/")
	else:
		form = BlogForm()
	return render_to_response('edit.html', {'form': form}, context_instance=RequestContext(request))


def about(request):
	return render_to_response("about.html", {})

def contact(request):
	return render_to_response("contact.html", {})

def resume(request):
	return render_to_response("resume.html", {})
















