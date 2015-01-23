"""Configures FancyWebcast."""

import json

def main():
    """The main method for this program."""

    config = {}
    config['event'] = {}
    config['event']['name'] = raw_input('Enter the tag for this event (e.g. "2015mnmi"): ');

    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)

main()
