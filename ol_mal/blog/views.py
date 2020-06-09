from django.shortcuts import render,get_object_or_404
from .models import *
from django.views.generic import View
from.utils import *
from .forms import TagForm, PostForm,DOIForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.core.paginator import Paginator


def post_list(request):
	posts = DOI.objects.all()
	paginator = Paginator(posts,10)
	page_number = request.GET.get('page', 1)
	page = paginator.get_page(page_number)

	is_paginated = page.has_other_pages()
	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''
	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''
	context = {
	'posts':page,
	'is_paginated' : is_paginated,
	'next_url': next_url,
	'prev_url': prev_url
	}
	return render(request,'blog/index.html',context = context)

class PostDetail(View,ObjectDetailMixin):
	model = Post
	template = 'blog/blog_detail.html'
	
def tags_list(request):
	search_query=request.GET.get('search','')
	l=[]
	for i in os.walk(settings.MEDIA_ROOT):
		l = i[2]
		if search_query:
			if search_query in l:
				l = [search_query]
		for j, j1 in enumerate(l):
			l[j] = '/media/'+j1
	 
	paginator = Paginator(l,10)
	page_number = request.GET.get('page', 1)
	page = paginator.get_page(page_number)

	is_paginated = page.has_other_pages()
	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''
	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''
	context = {
	'is_paginated' : is_paginated,
	'next_url': next_url,
	'prev_url': prev_url,
	'l':page
	}
	return render(request,'blog/tags_list.html',context=context)

class TagDetail(View,ObjectDetailMixin):
	model = Tag
	template = 'blog/tag_ditail.html'
	
class TagCreate(LoginRequiredMixin,View,ObjectCreatelMixin):
	model = TagForm
	template = 'blog/tag_create.html'
	raise_exception = True
	
class PostCreate(LoginRequiredMixin,View,ObjectCreatelMixin):
	model = DOIForm
	template = 'blog/post_create.html'
	raise_exception = True

class TagUpdate(LoginRequiredMixin,View,ObjectUpdateMixin):
	model = Tag
	modelForm = TagForm
	template = 'blog/tag_update_form.html'
	raise_exception = True

class PostUpdate(LoginRequiredMixin,View,ObjectUpdateMixin):
	model = Post
	modelForm = PostForm
	template = 'blog/post_update_form.html'
	raise_exception = True

class TagDelete(LoginRequiredMixin,View,ObjectDeleteMixin):
	model = Tag
	template = 'blog/tag_delete_form.html'
	url = 'tags_list_url'
	raise_exception = True

class PostDelete(LoginRequiredMixin,View,ObjectDeleteMixin):
	model = Post
	template = 'blog/post_delete_form.html'
	url = 'post_list_url'
	raise_exception = True
	
class Uploader(LoginRequiredMixin,View):
	def get(self,request):
		return render(request,'blog/upload.html')
	def post(self,request):
		upload_file = request.FILES['document']
		fs = FileSystemStorage()
		fs.save(upload_file.name,upload_file)
		return render(request,'blog/upload.html')
	raise_exception = True
