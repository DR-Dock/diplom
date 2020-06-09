from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time



def gen_slug(s):
	return slugify(s,allow_unicode=True)+'-'+str(int(time()))

class Post(models.Model):
	#file = models.FileField(upload_to="blog/DownloadsVOZ/",null=True,blank = True)
	title = models.CharField(max_length = 150, db_index = True)
	slug = models.SlugField(max_length = 150,blank=True,unique = True)
	body = models.TextField(blank = True,db_index = True)
	tags = models.ManyToManyField('Tag',blank = True, related_name = 'posts')
	date_pub = models.DateTimeField(auto_now_add = True)
	
	def save(self,*args,**kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args,**kwargs)

	def get_update_url(self):
		return reverse('post_update_url', kwargs = {'slug': self.slug})

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs = {'slug': self.slug})

	
	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs = {'slug': self.slug}) 

	def __str__(self):
		return'{}'.format(self.title)


class Tag(models.Model):
	title = models.CharField(max_length= 50)
	slug = models.SlugField(max_length = 50, unique=True)

	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs = {'slug': self.slug})

	def get_absolute_url(self):
		return reverse('tag_ditail_url', kwargs = {'slug': self.slug})

	def get_update_url(self):
		return reverse('tag_update_url', kwargs = {'slug': self.slug})

	def __str__(self):
		return '{}'.format(self.title)

class DOI(models.Model):
	doi = models.CharField(max_length= 150)


class pdfFile(models.Model):
	document = models.FileField(upload_to='documents/')