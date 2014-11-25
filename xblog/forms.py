from django.db import models
from django.forms import ModelForm

from models import Blog

class BlogForm(ModelForm):
	class Meta:
		model = Blog
		fields = ('caption', 'article_id', 'category', 'content')


