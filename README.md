# FancyWebcast
A webcast overlay system for the Fighting Calculators.

## Requirements

- Python 2.7+
- Google Chrome

## Setting up

On Windows, the Python applications may work when you double-click them. However, running them through a command prompt or terminal is recommended. If the `python` command does not work for you on Windows, make sure that Python is on your PATH. (http://stackoverflow.com/questions/6318156/adding-python-path-on-windows-7)

First run `python configure.py` and choose the `event` option. Enter the tag of the event as it appears on The Blue Alliance. (e.g. 2015mnmi2 or 2014arc.) You can then `quit` the configure interface.

The rest of the interaction is controlled through `controller.py`. Launch it with `python controller.py` and follow the instructions in the application.

The actual webcast visuals are displayed in a web browser. Currently only Google Chrome is supported using the following special instructions: You must launch Chrome with a special flag that allows it to directly access the filesystem. Follow the instructions at http://stackoverflow.com/questions/18586921/how-to-launch-html-using-chrome-at-allow-file-access-from-files-mode for now...I'll figure out nicer instructions later, and probably provide shortcuts/aliases that work for each platform.

Once Chrome is open with this option, open `in-match.html`. Place Chrome in full-screen mode on your secondary monitor. This should work just fine, and you can now have fancy webcast overlays just like the Citrus Circuits! 
