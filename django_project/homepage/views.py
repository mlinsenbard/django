# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render
from models import *
from forms import SpellForm
from sm.sm import mostEfficient
from difflib import SequenceMatcher as SQ
import sys
import random
import json

sys.path.insert(0, '/home/mlinsenbard/')
import vars

def home(request):
    return render_to_response('homepage/home.html',{},RequestContext(request))

def blog(request):
	# Learn Ajax you tease
	# for now, just getting ALL blog posts and displaying them
	blogs = BlogEntry.objects.all().order_by('-date')

	if request.method == "GET" and "tag" in request.GET:
		tag = request.GET["tag"];
		filteredBlogs = [];

		for blog in blogs:
			for btag in blog.tags.all():
				if tag == btag.subject:
					filteredBlogs.append(blog);

		if len(filteredBlogs) > 0:
			return render_to_response('homepage/blog.html',{'blogs':filteredBlogs, 'notag':False, 'filter':tag},RequestContext(request))
		else:
			return render_to_response('homepage/blog.html',{'blogs':filteredBlogs, 'notag':True, 'filter':tag},RequestContext(request))

	else:
		return render_to_response('homepage/blog.html',{'blogs':blogs},RequestContext(request))

def projects(request):
	# Learn Ajax you tease
	# for now, just getting ALL projects and displaying them
	projects = Project.objects.all().order_by('title')

	return render_to_response('homepage/projects.html',{'projects':projects},RequestContext(request))

def music(request):
	return render_to_response('homepage/music.html',{},RequestContext(request))

def contact(request):
	return render_to_response('homepage/contact.html',{},RequestContext(request))

def mxpo(request):
	return render_to_response('homepage/mxpo.html',{},RequestContext(request))

def lol(request):
	if request.method == "POST":
		form = SpellForm(request.POST)

		if form.is_valid():
			# Get values and call mostEfficient
			values = (form.cleaned_data['ad'],form.cleaned_data['ap'],form.cleaned_data['cdr'])
			topFive = mostEfficient(values)

			fi = {}
			fi['champion'] = topFive[0][0]
			fi['spell'] = topFive[0][1]['name']
			fi['dps'] = topFive[0][2]

			se = {}
			se['champion'] = topFive[1][0]
			se['spell'] = topFive[1][1]['name']
			se['dps'] = topFive[1][2]

			th = {}
			th['champion'] = topFive[2][0]
			th['spell'] = topFive[2][1]['name']
			th['dps'] = topFive[2][2]

			fo = {}
			fo['champion'] = topFive[3][0]
			fo['spell'] = topFive[3][1]['name']
			fo['dps'] = topFive[3][2]

			fif = {}
			fif['champion'] = topFive[4][0]
			fif['spell'] = topFive[4][1]['name']
			fif['dps'] = topFive[4][2]

			result=True

			return render_to_response('homepage/lol.html',
				{'result':result,
				'fi':fi,
				'se':se,
				'th':th,
				'fo':fo,
				'fif':fif},
				RequestContext(request))

		else:
			result = False
			return render_to_response('homepage/lol.html',{'sform': form, 'result':result},RequestContext(request))

	else:
		form = SpellForm()
		result = False

	return render_to_response('homepage/lol.html', {'sform': form, 'result': result},RequestContext(request))
