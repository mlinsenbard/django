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

@csrf_exempt
def fight(request):
	text = "SlackFight works like this: Type 'fight' then 'start' to start a fight, 'attack' to attack, 'heal' to heal, and 'end to end the fight."
	
	if request.method == "POST": 
		user_name = request.POST["user_name"]
		text = user_name
		query = request.POST["text"].split()

		if (len(query) > 4):
			action = query[1]
			text = "we made it"
			if (SQ(None, action, "start").ratio() > 0.8):
				if (len(current_fights) == 0 and len(query)>2):
					if (userInFight(user_name)):
						text = "You're already in a fight! Type 'fight end' to end your fight if you want to start a new one!"
					else:
						fight = startFight(user_name, query[2])
						text = "The battle between " + user_name + " and " + query[2] + " has begun!\n" + attack()
			elif (SQ(None, action, "heal").ratio() > 0.8):
				if (len(current_fights) == 0):
					text = "There are no current fights! Type 'fight start [username of person you're attacking]' to start a fight"
				elif (userInFight(user_name)):
					fight = userInFight(user_name)
					text = heal(fight, user_name)
			elif (SQ(None, action, "attack").ratio() > 0.8):
				if (len(current_fights) == 0):
					text = "There are no current fights! Type 'fight start [username of person you're attacking]' to start a fight"
				elif (userInFight(user_name)):
					fight = userInFight(user_name)
					text = attack(fight, user_name)
			elif (SQ(None, action, "end").ratio() > 0.8):
				fight = userInFight(user_name)
				if fight:
					text = user_name + " has cancelled their fight with " + fight.target
					fight.delete()
				else:
					text = "You can't end what you haven't started! Type 'fight start [username of person you're attacking]' to start a fight"

	return HttpResponse(json.dumps({"text":text}), content_type="application/json")

 # Returns a Fight if the user is currently in one
 # Otherwise, returns False 
def userInFight(username):
	curr_fights = Fights.objects.all()
	for f in curr_fights:
		if (f.instigator == username):
			return f
		elif (f.target == username):
			return f
	return False;

# Starts a fight
def startFight(instigator, target):
	fight = Fight()
	fight.instigator = instigator
	fight.target = target
	fight.save()
	return fight

# Returns the attack text for an attack and performs all post-attack logic
def attack(fight, username):
	if (fight.turn):
		curr_attacker = fight.instigator
	else:
		curr_attacker = fight.target

	if (username == curr_attacker):
		weapons = [{"name":"Glock", "type":"gun", "sound":"BLAT BLAT!", "damage":2}, 
						   {"name":"Revolver", "type":"gun", "sound":"BLAM!", "damage":4}, 
				           {"name":"AK-47", "type":"gun", "sound":"RATATATATAT!", "damage":3},
				           {"name":".50 Cal", "type":"gun", "sound":"BOOM!", "damage":6},
				           {"name":"RPG", "type":"explosive", "sound":"WHOOSH...BOOOOOOM!", "damage":8},
				           {"name":"Shank", "type":"blade", "sound":"SCHNK!", "damage":1},
				           {"name":"Brass Knuckle", "type":"blunt", "sound":"BIFF!", "damage":0.5},
				           {"name":"Crowbar", "type":"blunt", "sound":"Ouch, Gordon Freeman!", "damage":2},
				           {"name":"Baseball Bat", "type":"blunt", "sound":"SMACK!", "damage":2},
				           {"name":"Pillow", "type":"blunt", "sound":"fwomp.", "damage":0},
				           {"name":"Katana", "type":"blade", "sound":"SLASH!", "damage":3},
				           {"name":"Greatsword", "type":"blade", "sound":"SLICE!", "damage":5},
				           {"name":"Crossbow", "type":"pierce", "sound":"THUNK!", "damage":4},
				           {"name":"Axe", "type":"blade", "sound":"CHING!", "damage":3.5},
				           {"name":"Spear", "type":"pierce", "sound":"STAB!", "damage":3.5},
				           {"name":"Water Ballon", "type":"blunt", "sound":"SPLOOSH!", "damage":0},
				           {"name":"Nuke", "type":"explosive", "sound":"BOOOOOOOOOOOOOOOOOOOM, baby!", "damage":10},
				           {"name":"Fire Magic", "type":"magic", "sound":"FWOOSH!", "damage":6},
				           {"name":"Lightning Magic", "type":"magic", "sound":"BZZT!", "damage":6},
				           {"name":"Ice Magic", "type":"magic", "sound":"SHING!", "damage":6},
				           {"name":"Dark Magic", "type":"magic", "sound":"tHe ENd is NEar.", "damage":15},
				           {"name":"Light Magic", "type":"magic", "sound":"*Angel Chorus*", "damage":13}]

		weapon = weapons[random.randint(0, len(weapons)-1)]
		dmg = random.randint(1,6)*weapon["damage"]

		text = weapon["sound"] + " " + user_name + " rocked " + target + "'s block with a " + weapon["name"] + " for " + str(dmg) + " damage."
		
		if (fight.turn):
			fight.t_hp -= dmg
			fight.turn = not fight.turn
			fight.save()
			if (fight.t_hp <= 0):
				text = fight.instigator + " has won the fight!"
				fight.delete()
		else:
			fight.i_hp -= dmg
			fight.turn = not fight.turn
			fight.save()
			if (fight.i_hp <= 0):
				text = fight.target + " has won the fight!"
				fight.delete()
	else:
		text = "It's not your turn! You can't act!"

	return text

# Returns the heal text for a heal and performs all post-heal logic
def heal(fight, username):
	if (fight.turn):
		curr_attacker = fight.instigator
	else:
		curr_attacker = fight.target

	if (username == curr_attacker):
		heal_power = random.randint(1,6)*random.randint(1,6)
		text = username + " has healed for " + str(heal_power) + " hit points"

		if (fight.turn):
			fight.i_hp -= dmg
			fight.turn = not fight.turn
			fight.save()
		else:
			fight.t_hp -= dmg
			fight.turn = not fight.turn
			fight.save()
	else:
		text = "It's not your turn! You can't act!"

	return text

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
