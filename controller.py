"""The new and improved controller for FancyWebcast."""

from time import time, strftime, sleep
import json
import match
import matches

CONFIG = {}

def writeView(view):
    out = {'view': view}
    with open('view.json', 'w') as outfile:
        json.dump(out, outfile)

def loadConfig():
    global CONFIG
    f = open('config.json')
    CONFIG = json.load(f)
    f.close()

def getMatchManually():
    result = {}

    tag = raw_input("Enter the match tag: ")
    tag = match.parseTag(tag)
    result['key'] = CONFIG['event']['name'] + "_" + tag['tag']

    result['comp_level'] = tag['comp_level']
    result['match_number'] = tag['match_number']
    result['set_number'] = tag['set_number']

    result['alliances'] = {'red': {'score': 0}, 'blue': {'score': 0}}
    print "Enter red alliance teams: "
    red_1 = "frc" + raw_input("Red 1: ")
    red_2 = "frc" + raw_input("Red 2: ")
    red_3 = "frc" + raw_input("Red 3: ")
    print "Enter blue alliance teams: "
    blue_1 = "frc" + raw_input("Blue 1: ")
    blue_2 = "frc" + raw_input("Blue 2: ")
    blue_3 = "frc" + raw_input("Blue 3: ")
    result['alliances']['red']['teams'] = [red_1, red_2, red_3]
    result['alliances']['blue']['teams'] = [blue_1, blue_2, blue_3]

    return result;

def main():
    """The main method for this program."""

    mode = -1
    current_match = None
    all_matches = matches.loadMatchesFromFile()

    loadConfig()

    # The available modes for this program are:
    # -1: Make new match
    # 0: Match ready
    # 1.1: Match running (auto)
    # 1.2: Match running (teleop)
    # 2: Match ended
    # 3: Match canceled
    # 4: Match results
    # 5: Upcoming match
    # 6.1: Pre-Match Rankings
    # 6.2: Post-Match Rankings

    while True:
        print "\n\n"

        match.writeLiveMatch(current_match)

        if mode == -1:
            # Load new match

            print "Now creating a new match."

            command = raw_input("Load match from online? (y / n): ")

            if command == "y":
                match_name = raw_input('Enter the tag for this match (e.g. "qm1" or "f2"): ')
                current_match = match.getLiveMatchFromOnline(CONFIG['event']['name'], match_name)
            else:
                print "Entering the match manually."
                try:
                    current_match = getMatchManually()
                except RuntimeError, e:
                    print e
                    continue

            current_match['match_running'] = False
            current_match['alliances']['red']['score'] = 0
            current_match['alliances']['blue']['score'] = 0

            mode = 0
        elif mode == 0:
            # Match ready

            writeView("match")

            print "Ready to start match:"
            print match.liveMatchStr(current_match)

            print "\nAvailable commands:"
            print "start\t- Starts the match"
            print "new\t- Creates or loads a new match"
            print "r\t- Switches to rankings"
            print "u\t- Switches to upcoming match view"

            command = raw_input("Enter your command: ")

            if command == "start":
                confirm = raw_input("Are you sure you want to start the match? (y / n): ")
                if confirm == "y":
                    raw_input("Press enter to start the match.")
                    current_match['start_time'] = time() * 1000
                    current_match['match_running'] = True
                    print "Match started at " + strftime("%I:%M:%S") + "."
                    mode = 1.1
            elif command == "new":
                mode = -1
            elif command == "r":
                mode = 6
            elif command == "u":
                mode = 5
            else:
                print "Unknown command."
        elif mode == 1.1:
            sleep(10)
            raw_input("Press enter once teleop begins.");
            current_match['teleop_time'] = time() * 1000
            mode = 1.2;
        elif mode == 1.2:
            # Match running

            print "Match in progress:"
            print match.liveMatchStr(current_match)

            print "\nAvailable commands:"
            print "r\t- Edits red alliance score"
            print "b\t- Edits blue alliance score"
            print "c\t- Shows or hides the Coopertition icon"
            print "end\t- Ends the match. (Match ended normally)"
            print "cancel\t- Cancels the current match. (Match was canceled by the refs)"

            command = raw_input("Enter your command: ")

            if command == "r":
                rs = raw_input("Enter new red score: ")
                try:
                    rs_int = int(rs)
                    current_match['alliances']['red']['score'] = rs_int
                except Exception:
                    print '"' + rs + '" is not a valid score.'
            elif command == "b":
                bs = raw_input("Enter new blue score: ")
                try:
                    bs_int = int(bs)
                    current_match['alliances']['blue']['score'] = bs_int
                except Exception:
                    print '"' + bs + '" is not a valid score.'
            elif command == "c":
                c = raw_input("Show Coopertition icon? (y/n): ");
                if c == "y":
                    current_match['coopertition_achieved'] = True
                else:
                    current_match['coopertition_achieved'] = False
            elif command == "end":
                current_match['match_running'] = False
                mode = 2
            elif command == "cancel":
                current_match['match_running'] = False
                print "Match canceled."
                mode = 3
            else:
                print "Unknown command."
        elif mode == 2:
            # Match ended

            print "Match ended:"
            print match.liveMatchStr(current_match)
            raw_input("Press enter when the final score goes up onscreen.")

            # Display "final score coming soon" thing

            ra = int(raw_input("Red auto: "))
            rt = int(raw_input("Red tote: "))
            rc = int(raw_input("Red container: "))
            rl = int(raw_input("Red litter: "))
            rf = abs(int(raw_input("Red foul: "))) * -1
            rtot = int(raw_input("Red total score: "))

            ba = int(raw_input("Blue auto: "))
            bt = int(raw_input("Blue tote: "))
            bc = int(raw_input("Blue container: "))
            bl = int(raw_input("Blue litter: "))
            bf = abs(int(raw_input("Blue foul: "))) * -1
            btot = int(raw_input("Blue total score: "))

            current_match['alliances']['red']['score'] = rtot
            current_match['alliances']['blue']['score'] = btot
            current_match['alliances']['red']['score_breakdown'] = {
                'auto': ra,
                'tote': rt,
                'container': rc,
                'container': rl,
                'foul': rf,
            }
            current_match['alliances']['blue']['score_breakdown'] = {
                'auto': ba,
                'tote': bt,
                'container': bc,
                'container': bl,
                'foul': bf,
            }

            matches.addMatchToMatches(current_match, all_matches)

            mode = 4
        elif mode == 3:
            # Match canceled

            print "Match canceled."

            print "\nAvailable commands:"
            print "new\t- Creates or loads a new match"
            print "r\t- Switches to rankings"
            print "u\t- Switches to upcoming match view"

            command = raw_input("Enter your command: ")

            if command == "new":
                mode = -1
            elif command == "r":
                mode = 6
            elif command == "u":
                mode = 5
            else:
                print "Unknown command."
        elif mode == 4:
            # Match results

            writeView("results")

            print "Now displaying match results."
            # Display match info here

            print "\nAvailable commands:"
            print "new\t- Creates or loads a new match"
            print "r\t- Switches to rankings"
            print "u\t- Switches to upcoming match view"

            command = raw_input("Enter your command: ")

            if command == "new":
                mode = -1
            elif command == "r":
                mode = 6
            elif command == "u":
                mode = 5
            else:
                print "Unknown command."
        elif mode == 5:
            # Upcoming match view

            writeView("upcoming")

            print "Now displaying upcoming match view."
            # Display match info here

            print "\nAvailable commands:"
            print "new\t- Creates or loads a new match"
            print "r\t- Switches to rankings"

            command = raw_input("Enter your command: ")

            if command == "new":
                mode = -1
            elif command == "r":
                mode = 6
            else:
                print "Unknown command."
        elif mode == 6:
            # Rankings view

            writeView("rankings")

            print "Now displaying rankings."

            print "\nAvailable commands:"
            print "new\t- Creates or loads a new match"
            print "u\t- Switches to upcoming match view"

            command = raw_input("Enter your command: ")

            if command == "new":
                mode = -1
            elif command == "u":
                mode = 5
            else:
                print "Unknown command."

main()
