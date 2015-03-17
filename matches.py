"""A class which will manage the JSON file containing all the match results from an event."""

import json
import urllib2

POSTFIX = "?X-TBA-App-Id=2175:FancyWebcast:0.1"

def loadMatchesFromFile():
    try:
        f = open('matches.json')
    except IOError, e:
        writeMatches([])
    
    f = open('matches.json')
    matches = json.load(f)
    f.close()
    return matches

def loadMatchesFromOnline(event):
    response = urllib2.urlopen("http://www.thebluealliance.com/api/v2/event/" + event + "/matches" + POSTFIX).read()
    matches = json.loads(response)
    return matches

def addMatchToMatches(match, matches):
    matchesWithNumber = [m for m in matches if m['key'] == match['key']]
    
    if len(matchesWithNumber) != 0:
        for m in matchesWithNumber:
            matches.remove(m)
    matches.append(match)

def writeMatches(matchesObject):
    with open('matches.json', 'w') as outfile:
        json.dump(matchesObject, outfile)