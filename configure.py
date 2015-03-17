"""Configures FancyWebcast."""

import json
import matches

def main():
    """The main method for this program."""

    while True:

        print "\nAvailable commands:"
        print "event\t- Loads new event data."
        print "matches\t- Loads match results from The Blue Alliance."
        print "quit\t- Quit"

        command = raw_input("Enter your command: ")

        if command == "event":
            config = {}
            config['event'] = {}
            config['event']['name'] = raw_input('Enter the tag for this event (e.g. "2015mnmi"): ');

            with open('config.json', 'w') as outfile:
                json.dump(config, outfile)
        elif command == "matches":
            name = raw_input("Enter the event tag (e.g. \"2015mnmi\"): ")
            theMatches = matches.loadMatchesFromOnline(name)
            matches.writeMatches(theMatches)
        elif command == "quit":
            break;

main()
