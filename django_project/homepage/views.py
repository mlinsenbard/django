# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from models import *
from forms import SpellForm
from sm.sm import mostEfficient

def home(request):
    return render_to_response('homepage/home.html',{},RequestContext(request))

def blog(request):
	# Learn Ajax you tease
	# for now, just getting ALL blog posts and displaying them
	blogs = BlogEntry.objects.all().order_by('-date')

	return render_to_response('homepage/blog.html',{'blogs':blogs},RequestContext(request))

def programming(request):
	# Learn Ajax you tease
	# for now, just getting ALL projects and displaying them
	projects = Project.objects.all().order_by('title')

	return render_to_response('homepage/programming.html',{'projects':projects},RequestContext(request))

def music(request):
	return render_to_response('homepage/music.html',{},RequestContext(request))

def contact(request):
	return render_to_response('homepage/contact.html',{},RequestContext(request))

def lol(request):
	if request.method == "POST":
		form = SpellForm(request.POST)

		if form.is_valid():
			# Get values and call mostEfficient
			values = (form.cleaned_data['ad'],form.cleaned_data['ap'],form.cleaned_data['cdr'])
			result = mostEfficient(values)

			champion = result[0]
			spell = result[1]['name']
			dps = result[2]

			result = True

			return render_to_response('homepage/lol.html',{'result':result, 
				'champion':champion, 
				'spell':spell,
				'dps':dps},RequestContext(request))

		else:
			result = False
			return render_to_response('homepage/lol.html',{'sform': form, 'result':result},RequestContext(request))

	else:
		form = SpellForm()
		result = False

	return render_to_response('homepage/lol.html', {'sform': form, 'result': result},RequestContext(request))
