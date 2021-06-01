"""
Some config, that can be setup globally for not having to use in each function call.

Config values are:

TO_FILE - Whether log to file or warn to console.

AROUND - If log to file, whether separate logs with line breaks and ==== or shring to save space.
Defaults to True.

COLOR - Colorize is automated. If to console, it is colorized, if to file, it's not (.log files
can be colorized by IDE). Defaults to 'auto'.

"""

TO_FILE = False  # Whether log to file. Setup str path (or pathlib.Path) of file
#   with .log suffix (create if not exist). Print to console then doesn't work
AROUND = "auto"  # Separate logs with ===== and line breaks for better visibility.
#   If 'auto', then if TO_FILE = True, then AROUND = False, if TO_FILE = False, AROUND = True.
COLOR = "auto"  # Whether colorize results - mostly python syntax in tracebacks. If _TO_FILE is configured, colorize is ignored.


# Do not edit, internal variables
__DEBUG = 1
