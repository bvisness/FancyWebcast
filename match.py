"""Stuff related to FRC matches."""

import time
import json
import urllib2
import collections

import score

POSTFIX = "?X-TBA-App-Id=2175:FancyWebcast:0.1"

def getLiveMatchFromFile():
    match = {}
    f = open('match.json')
    match = json.load(f)
    f.close()
    return match

def getLiveMatchFromOnline(event, number):
    key = event + "_" + number
    response = urllib2.urlopen("http://www.thebluealliance.com/api/v2/match/" + key + POSTFIX).read()
    match = json.loads(response)
    return match

def getLiveMatchScores():
    match = getLiveMatchFromFile()
    return (match['alliances']['red']['score'], match['alliances']['blue']['score'])

def writeLiveMatch(match):
    with open('match.json', 'w') as outfile:
        json.dump(match, outfile)

def liveMatchStr(match):
    result = "Match key: " + match['key'] + "\n"
    if 'start_time' in match:
        result += "Match started at " + time.strftime("%I:%M:%S", time.localtime(match['start_time'] / 1000)) + "\n"
    result += "Red: " + str(match['alliances']['red']['score']) + "\t\tBlue: " + str(match['alliances']['blue']['score']) + "\n"
    result += "Red teams:\tBlue Teams:\n"
    for i in range(0, 3):
        result += "- " + match['alliances']['red']['teams'][i] + "\t- " + match['alliances']['blue']['teams'][i] + "\n"

    return result
