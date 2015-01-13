import csv

class Match:
	fieldnames = ['number', 'starttime', 'redscore', 'bluescore']

	def __init__(self,number=0,starttime=0,redscore=0,bluescore=0):
		self.number = number
		self.starttime = starttime
		self.redscore = redscore
		self.bluescore = bluescore

def getMatchFromFile():
	match = Match()
	with open('match.csv', 'rb') as f:
		reader = csv.DictReader(f)
		for row in reader:
			match = Match(row['number'],row['starttime'],row['redscore'],row['bluescore'])
			break
	return match

def getScores():
	match = getMatch()
	return (match.redscore, match.bluescore)

def writeMatch(match):
	with open('match.csv', 'w') as csvfile:
		fieldnames = Match.fieldnames
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		writer.writerow({'number': match.number, 'starttime': match.starttime, 'redscore': match.redscore, 'bluescore': match.bluescore})

def getMatchFromOnline(event, number):
	# Use TBA or FMS API to get match with given number
	return