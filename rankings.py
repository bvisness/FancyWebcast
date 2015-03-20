# This class will calculate rankings based on a list of matches, in the format expected by matches.py. This class produces and works with a list of teams in the following format:

# [
# 	{
# 		number: 'frc2175',
# 		qualification_average: XXX,
# 		qualification_sum: XXX,
# 		coopertition_sum: XXX,
# 		auto_sum: XXX,
# 		container_sum: XXX,
# 		tote_sum: XXX,
# 		litter_sum: XXX,
#		played: X,
# 	},
# 	...
# ]

import urllib2
import json

import matches

POSTFIX = "?X-TBA-App-Id=2175:FancyWebcast:0.1"

def loadRankingsFromOnline(event):
	"""Loads ranking information from The Blue Alliance. It is modified to fit the nicer object-array format that this program uses."""

	response = urllib2.urlopen("http://www.thebluealliance.com/api/v2/event/" + event + "/rankings" + POSTFIX).read()
	rankings = json.loads(response)

	realRankings = []
	realRankings.append({})
	for i in range(1, len(rankings) - 1):
		realRankings.append({
			'number': rankings[i][1],
			'qualification_average': rankings[i][2],
			'auto_sum': rankings[i][3],
			'container_sum': rankings[i][4],
			'coopertition_sum': rankings[i][5],
			'litter_sum': rankings[i][6],
			'tote_sum': rankings[i][7],
			'played': rankings[i][8],
		})

	return realRankings

def updateTeamInfo(teams, matches):
	"""Calculates the teams' score sums and qualification averages from a list of matches. UNTESTED"""

	# Reset each team's scoring info
	for team in teams:
		team['qualification_sum'] = 0
		team['coopertition_sum'] = 0
		team['auto_sum'] = 0
		team['container_sum'] = 0
		team['tote_sum'] = 0
		team['litter_sum'] = 0
		team['played'] = 0

	# Only examine matches that have a score breakdown.
	# (Matches produced by this webcast system.)
	matches = [x for x in matches if x['alliances']['blue'].has_key('score_breakdown')]

	for match in matches:
		# Get all the teams that played this match, and for which this
		# was not a surrogate match
		matchTeams = match['alliances']['blue']['teams'] + match['alliances']['red']['teams']
		if match['alliances'].has_key('surrogates'):
			matchTeams = [x for x in matchTeams if x not in match['alliances']['surrogates']]

		for matchTeam in matchTeams:
			# Determine the team's color in this match.
			color = None
			if matchTeam in match['alliances']['red']['teams']:
				color = 'red'
			else:
				color = 'blue'

			# Get the matching entry/entries for this team.
			teamEntries = [x for x in teams if x['number'] == matchTeam]

			# Handle exceptions
			if len(teamEntries) == 0:
				raise Exception("No entry for " + matchTeam + " exists.")
			if len(teamEntries) > 1:
				raise Exception("Duplicate entries for " + matchTeam + " exist.")

			teamEntry = teamEntries[0]

			# Add the score information to this team's entry.
			score = match['alliances'][color]['score']
			breakdown = match['alliances'][color]['score_breakdown']
			teamEntry['qualification_sum'] += score
			teamEntry['coopertition_sum'] += breakdown['coopertition']
			teamEntry['auto_sum'] += breakdown['auto']
			teamEntry['container_sum'] += breakdown['container']
			teamEntry['tote_sum'] += breakdown['tote']
			teamEntry['litter_sum'] += breakdown['litter']
			teamEntry['played'] += 1 

	for team in teams:
		team['qualification_average'] = team['qualification_sum'] / team['played']

	return teams

#TODO Add a method that actually produces a rankings array from the information above!
