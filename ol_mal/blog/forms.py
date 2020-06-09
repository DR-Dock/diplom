from django import forms
from .models import Tag, Post, DOI
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','slug','body','tags']
		widgets = {
		'title':forms.TextInput(attrs={'class':'form-control'}),
		'slug':forms.TextInput(attrs={'class':'form-control'}),
		'body':forms.Textarea(attrs={'class':'form-control'}),
		'tags':forms.SelectMultiple(attrs={'class':'form-control'}),
		}
	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()
		if new_slug == 'create':
			raise ValidationError("Slug may not be create")
		if Post.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))
		return new_slug


			

class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['title','slug']

		widgets = {
		'title':forms.TextInput(attrs={'class':'form-control'}),
		'slug':forms.TextInput(attrs={'class':'form-control'}),
		}

	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()
		if new_slug == 'create':
			raise ValidationError('Slug may not be create')
		if Tag.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))
		return new_slug




class DOIForm(forms.ModelForm):
	class Meta:
		model = DOI
		fields = ['doi']
		widgets = {
		'doi':forms.TextInput(attrs={'class':'form-control'})
		}
	def clean_doi(self):
		new_doi = self.cleaned_data['doi'].lower()
		if DOI.objects.filter(doi__iexact=new_doi).count():
			raise ValidationError('DOI must be unique. We have "{}" DOI already'.format(new_doi))
		return new_doi