from django.shortcuts import render,get_object_or_404
from .models import *
from django.shortcuts import redirect

class ObjectDetailMixin:
	model = None
	template = None

	def get(self,request,slug):
		obj = get_object_or_404(self.model, slug__iexact=slug)
		return render(request, self.template,context={self.model.__name__.lower():obj,'admin_object':obj,'detail':True})


class ObjectCreatelMixin:
	model = None
	template = None
	def get(self,request):
		form = self.model()
		return render(request,self.template, context={'form':form})
	def post(self,request):
		bound_form = self.model(request.POST)
		if bound_form.is_valid():
			new_post = bound_form.save()
			#return redirect(new_post)
		return render(request,self.template, context={'form':bound_form})

class ObjectUpdateMixin:
	modelForm = None
	model = None
	template = None
	def post(self,request,slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.modelForm(request.POST,instance = obj)
		
		if bound_form.is_valid():
			new_obj = bound_form.save()
			return redirect(new_obj)
		return render(request,self.template,context={'form':bound_form,self.model.__name__.lower():obj})
	
	def get(self,request,slug):
		obj = self.model.objects.get(slug__iexact=slug)
		bound_form = self.modelForm(instance=obj)
		return render(request,self.template,context={'form':bound_form,self.model.__name__.lower():obj})

class ObjectDeleteMixin:
	model = None
	template = None
	url = None
	def get(self,request,slug):
		obj = self.model.objects.get(slug__iexact = slug)
		return render(request,self.template,context={self.model.__name__.lower():obj})
	def post(self,request,slug):
		obj = self.model.objects.get(slug__iexact = slug)
		obj.delete()
		return redirect(reverse(self.url))
