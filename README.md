# mylogging

[![Python versions](https://img.shields.io/pypi/pyversions/mylogging.svg)](https://pypi.python.org/pypi/mylogging/) [![PyPI version](https://badge.fury.io/py/mylogging.svg)](https://badge.fury.io/py/mylogging) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Malachov/mylogging.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Malachov/mylogging/context:python) [![Documentation Status](https://readthedocs.org/projects/mylogging/badge/?version=latest)](https://mylogging.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/Malachov/mylogging/branch/master/graph/badge.svg)](https://codecov.io/gh/Malachov/mylogging)

My python warn-logging module. Based on debug value prints and logs warnings and errors. It's automatically colorized.
It log to console or it can log to file if configured.

Motivation for this project is to be able to have one very simple code base for logging and warning at once.
You can use one code for logging apps running on server (developer see if problems) and the same code for
info and warnings from running python code on computer in some developed library (user see when using code).

One code, two use cases.

Other reasons are to be able to recognise immediately if error is from my library or from some imported library.
Library try to be the simplest for use as possible (much simplier than logging or logguru).
Library have user friendly formatting.

## Installation

Python >=3.6 (Python 2 is not supported).

Install just with

```console
pip install mylogging
```

## Examples

### Example set_warnings

This will configure what warnings will be displayed.

If log to console, override warnings display globally!!! => It's used mostly for developing - debugging apps
(do not use in set_warnings in python libraries that other imports - you could redefined his warnings filters).

If logging to file (good for web servers), warning levels are ignored!!! you don't have to call this function.

```python
import mylogging
mylogging.set_warnings(debug=1)
```

- ignore warnings: debug=0,
- display warnings once: debug=1,
- display warnings always: debug=2,
- stop warnings as errors: debug=3

You can ignore some warnings just by pass list of ignored warnings (any part of warning message suffice)
just add `ignored_warnings=["invalid value encountered in sqrt", "another ignored..."]` arg.

### Example of warnings and logginng - info, warn, traceback

```python
import mylogging

mylogging.set_warnings()

mylogging.warn('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")
```

We can log / warn tracebacks from expected errors and continue runtime.

```python
try:
    print(10 / 0)

except ZeroDivisionError:
    mylogging.traceback("Maybe try to use something different than 0.")
```

Info will not trigger warning, but just print to console (but follows the rule in set_warnings(debug)).

```python
mylogging.info("I am interesting info")
```

## Logging to file

If you want to log to file, it's very simple just edit 'TO_FILE' to path with suffix (file will
be created if not exist).

```python
import mylogging

mylogging.config.TO_FILE = "path/to/my/file.log"  # You can use relative (just log.log)
```

Then it's the same

```python
import mylogging

mylogging.warn('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

try:
    print(10 / 0)
except ZeroDivisionError:
    mylogging.traceback("Maybe try to use something different than 0.")
```

You can use captions as well

```python
mylogging.info("I am interesting info", caption="I am caption")
```

There is one more function you can use: `return_str`. It will return edited string (Color, indent and around signs).
Use case for that is raising your errors. You can see in one second, whether raise is yours or from imported library.

```python
raise ModuleNotFoundError(mylogging.return_str("It's not in requirements because...", caption="Library not installed error"))
```

## config

There is many things that is better to set globally than setup in each function call.

### AROUND

If log to file, whether separate logs with line breaks and ==== or shring to save space.
Defaults to True.

### COLOR

You can turn off colors if you need (somewhere symbols instead of colors are displayed).
"auto" by default means: If to console, it is colorized, if to file, it's not (.log files
can be colorized by IDE).

If you have special use case (for example pytest logs on CI/CD), you can override value from auto

```python
mylogging.config.COLORIZE = False # Turn off colorization on all functions to get rid of weird symbols
```

This is how the results in console look like.

<p align="center">
<img src="docs/source/_static/logging.png" width="620" alt="Logging output example"/>
</p>

For log file, just open example.log in your IDE.
This is how the results in log file opened in VS Code look like.

<p align="center">
<img src="docs/source/_static/logging_file.png" width="620" alt="Logging to file example"/>
</p>
