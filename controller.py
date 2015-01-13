# ----------------------------
# FancyWebcast Controller
# ----------------------------

from time import time, gmtime, strftime

import match

theMatch = match.Match()

def initController():
	global theMatch
	theMatch = match.getMatchFromFile()

def initMatch():
	global theMatch
	theMatch.redscore = 0
	theMatch.bluescore = 0
	theMatch.starttime = time() * 1000
	match.writeMatch(theMatch)

def printMatch():
	print "\n"
	print "Red score: " + str(theMatch.redscore)
	print "Blue score: " + str(theMatch.bluescore)
	print "\n"

def main():
	global theMatch

	initController()

	while (True):
		printMatch()

		command = raw_input('Enter a command (h for help): ')
		
		if command == "n":
			confirm = raw_input("Are you sure? (y / n): ")
			if confirm == "y":
				raw_input("Press enter to start the match.");
				initMatch()
				print "Match started at " + strftime("%I:%M:%S") + "."
		elif command == "h":
			print "n:\tStarts a new match."
			print "s:\tEdits scores."
			print "exit:\tExits the program."
		elif command == "s":
			theMatch.redscore = raw_input("Red score: ")
			theMatch.bluescore = raw_input("Blue score: ")
			match.writeMatch(theMatch)
		elif command == "exit":
			exit()

main()