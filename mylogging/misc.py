"""
This module is internal module for mylogging library. It's not supposed to be used by user.
"""

from datetime import datetime
import warnings
import sys
from . import config


printed_infos = set()
original_showwarning = warnings.showwarning


def log_warn(message, log_type, showwarning_details=True):
    """If _TO_FILE is configured, it will log message into file on path _TO_FILE. If not _TO_FILE is configured, it will
    warn or print INFO message.

    Args:
        message (str): Any string content of warning.
        log_type (str): 'INFO' or something else, generated automatically from __init__ module.
        edit_showwarning (bool): Whether to override warnings details display. After warning, default one will be again used.
            Defaults to True.
    """

    if config.TO_FILE:
        with open(config.TO_FILE, "a+") as f:
            f.write(
                f"{datetime.now().strftime(r'%d/%m/%Y %H:%M:%S')} {log_type} {message}"
            )

    else:
        if log_type == "INFO":
            if config.__DEBUG == 1:
                if message not in printed_infos:
                    print(message)
                    printed_infos.add(message)
            elif config.__DEBUG > 1:
                print(message)

        else:

            if showwarning_details:
                warnings.showwarning = showwarning_detailed

            else:
                warnings.showwarning = showwarning_stripped

            warnings.warn(message, stacklevel=3)

            warnings.showwarning = original_showwarning


def objectize_str(message):
    """Make a class from a string to be able to apply escape characters and colors if raise.

    Args:
        message (str): Any string you use.

    Returns:
        Object: Object, that can return string if printed or used in warning or raise.
    """

    class X(str):
        def __repr__(self):
            return f"{message}"

    return X(message)


def colorize(message):
    """Add color to message - usally warnings and errors, to know what is internal error on first sight.
    Simple string edit.

    Args:
        message (str): Any string you want to color.

    Returns:
        str: Message in yellow color. Symbols added to string cannot be read in some terminals.
            If config COLOR is 0, it return original string.
    """

    if config.COLOR in [True, 1] or (config.COLOR == "auto" and not config.TO_FILE):

        return f"\033[93m {message} \033[0m"

    else:
        return message


def showwarning_detailed(message, category, filename, lineno, *args, **kwargs):
    """Function that can override warnings printed info. """

    sys.stderr.write(f"\n\n{category.__name__} from {filename}:{lineno} {message}\n")


def showwarning_stripped(message, *args, **kwargs):
    """Function that can override warnings printed info."""

    sys.stderr.write(f"{message}\n")
