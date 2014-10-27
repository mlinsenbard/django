# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import *

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