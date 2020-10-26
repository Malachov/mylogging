# mylogging

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mylogging.svg)](https://pypi.python.org/pypi/mylogging/) [![PyPI version](https://badge.fury.io/py/mylogging.svg)](https://badge.fury.io/py/mylogging) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Malachov/mylogging.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Malachov/mylogging/context:python) [![Build Status](https://travis-ci.com/Malachov/mylogging.svg?branch=master)](https://travis-ci.com/Malachov/mylogging) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/Malachov/mylogging/branch/master/graph/badge.svg)](https://codecov.io/gh/Malachov/mylogging)

My python logging module not only for new python libraries. Based on debug value prints warnings and errors. It's automatically colorized. It can be logged to file if configured (then color ignored).

Documentation does not exists, because it's such a small project, that it's not necessary - everything important is in this readme (and in the docstrings for developers).

Motivation for this project is to create simplest logging module that do everytthing I need.

## Example

```python
import mylogging

# We can define whether to
#   display warnings: debug=1,
#   ignore warnings: debug=0,
#   stop warnings as errors: debug=3

mylogging.set_warnings(debug=1, ignored_warnings=["invalid value encountered in sqrt",
                                                 "encountered in double_scalars"])

# We can create warning that will be displayed based on warning settings
mylogging.user_warning('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

# In case we don't know exact error reason, we can use traceback_warning in try/except block

try:
    u = 10 / 0

except Exception:
    mylogging.traceback_warning("Maybe try to use something different than 0")


# In case we don't want to warn, but we have error that should be printed anyway and not based on warning settings, we can use user_message that return extended string that we can use...

print(mylogger.user_message("I will be printed anyway"))

# If you want to log to file, just add the path (with log suffix) on the beginning

mylogging._TO_FILE = "path/to/my/file.log"

```

This is the result of the upper snippet

<p align="center">
<img src="logging.png" width="620" alt="Plot of results"/>
</p>

If colors are not wanted (resulting weird symbols) you can use this after the import

```python
mylogging._COLORIZE = 0  # Turn off colorization on all functions
```
