from urllib2 import urlopen
import collections
import json
import sys, os
from sm_special import DISREGARDED_SPELLS, SPECIAL_SPELLS

###########
# GLOBALS #
###########

# Used to access 3-tuple variables by name
AD = 0
AP = 1
CDR = 2

# Obtains all Champion data for use in functions
# API Key would normally be kept secret but is hard-coded to ensure this script works on any machine
sys.path.insert(0, '/home/mlinsenbard/')
import vars
result = urlopen(
	"https://na.api.pvp.net/api/lol/static-data/na/v1.2/champion?locale=en_US&champData=spells&api_key="+vars.API_KEY)
ALL_CHAMPS = json.loads(result.read())['data']

#############
# FUNCTIONS #
#############

#############################
# getNukeDPS
#
# Input: spell [dict], values [3-tuple]
# Output: dps [float]
# 
# Grabs the correct values and computes
# the DPS of a standard 'nuke' spell
#############################
def getNukeDPS(spell, values):
	# Finding the 'Damage' tag in leveltip helps figure 
	# out which 'effect' index our damage values are in
	for i,l in enumerate(spell['leveltip']['label']):
		if 'Damage' in l:
			maxLevel = int(spell['maxrank'])

			# go char by char to find x in 'ex'
			# in "effect":["{{ e1 }} -> {{ e1NL }}",
			for c in spell['leveltip']['effect'][i]:
				if c.isnumeric():
					damageIndex = int(c)
					break
			# Using the maxlevel var and index, get our base damage value for the spell
			damageVal = float(spell['effect'][damageIndex][maxLevel-1])
			cooldown = int(spell['cooldown'][maxLevel-1])

			apRatio = 0
			adRatio = 0
			bonusADRatio = 0
			try:
				# get AD/AP scaling coeffecients
				for var in spell['vars']:
					if 'attackdamage' in var['link'] and adRatio == 0:
						adRatio = float(var['coeff'][0])
					elif 'spelldamage' in var['link'] and apRatio == 0:
						apRatio = float(var['coeff'][0])
					elif 'bonusattackdamage' in var['link'] and adRatio == 0:
						bonusADRatio = float(var['coeff'][0])
			except:
				# Spell has no coeffs
				pass

			# We have our damage, cooldown, and ratios. Time to calculate dps
			totalDamage = damageVal + (apRatio * values[AP]) + (adRatio * values[AD]) + (bonusADRatio * values[AD])
			try:
				dps = totalDamage/(cooldown-(cooldown*(values[CDR]/100)))
			except Exception:
				# Return -1 to signify error
				dps = -1

			return dps

#############################
# mostEfficient
#
# Input: 3-Tuple (AD [float], AP [float], CDR [float])
# Output: 3-Tuple (champion [dict], spell [dict], DPS [float])
# 
# Calculates the spell with
# highest DPS given AD/AP/CDR
#############################
def mostEfficient(values):
	topFive = [None, None, None, None, None]
	bestSpellDPS = [0,0,0,0,0]

	# Open resutls file for reading
	fp = open('..\..\static\files\results.txt', 'w')
	s = "AD: "+str(values[0])+" AP: "+str(values[1])+" CDR: "+str(values[2])+"\n\n"
	fp.write(s)
	sortedChamps = collections.OrderedDict(sorted(ALL_CHAMPS.items()))
	for k,v in sortedChamps.iteritems():
		fp.write(k)
		fp.write('\n')
		for s in v['spells']:
			# If the spell isnt even to be considered, do nothing
			if s['name'] in DISREGARDED_SPELLS:
				pass
			else:
				try:
					# Try seeing if a special case function exists
					dps = SPECIAL_SPELLS[s['name']](values)
				except Exception:
					# Run normal data scraping & calculations
					dps = getNukeDPS(s, values)

				# Working on getting top 5
				currTuple = (k,s,dps)
				fp.write(s['name'])
				fp.write('\n')
				fp.write(str(dps))
				fp.write('\n\n')
				for i, d in enumerate(bestSpellDPS):
					if d == 0 and not topFive[i]:
						# Base case for if there are no values yet
						bestSpellDPS[i] = dps
						topFive[i] = currTuple
						break
					elif dps > d:
						# swap dps and d
						t = bestSpellDPS[i]
						bestSpellDPS[i] = dps
						dps = t
						# swap currTuple and topFive[i]
						t = topFive[i]
						topFive[i] = currTuple
						currTuple = t
		fp.write('\n')

	# Do a sanity check to make sure we have a top 5 filled out
	fp.close()
	return topFive









