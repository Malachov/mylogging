import warnings
import traceback
import textwrap
import os
import pygments

# To enable colors in cmd...
os.system('')

_COLORIZE = 0


def objectize_str(message):
    """Make a class from a string to be able to apply escape characters and colors in tracebacks.

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
            If global _COLORIZE is 0, it return original string.
    """

    return f"\033[93m {message} \033[0m"


def user_message(message, caption="User message"):
    """Return enhanced colored message. Used for raising exceptions, assertions or important warninfs mainly.
    You can print returned message, or you can use user_warning function. Then it will be printed only in debug mode.

    Args:
        message (str): Any string content of warning.

    Returns:
        enhanced
    """
    updated_str = textwrap.indent(text=f"\n\n========= {caption} ========= \n\n {message} \n\n", prefix='    ')

    if _COLORIZE:
        updated_str = colorize(updated_str)

    return objectize_str(updated_str)


def user_warning(message, caption="User message"):
    """Raise warning - just message, not traceback. Can be colorized. Display of warning is configured with debug variable in `config.py`.

    Args:
        message (str): Any string content of warning.
    """

    warnings.warn(user_message(message, caption=caption))


def traceback_warning(message='Traceback warning'):
    """Raise warning with current traceback as content. There is many models in this library and with some
    configuration some models crashes. Actually it's not error than, but warning. Display of warning is
    configured with debug variable in `config.py`.

    Args:
        message (str, optional): Caption of warning. Defaults to 'Traceback warning'.
    """
    if _COLORIZE:
        separated_traceback = pygments.highlight(traceback.format_exc(), pygments.lexers.PythonTracebackLexer(), pygments.formatters.Terminal256Formatter(style='friendly'))
    else:
        separated_traceback = traceback.format_exc()

    separated_traceback = textwrap.indent(text=f"\n\n{message}\n====================\n\n{separated_traceback}\n====================\n", prefix='    ')

    warnings.warn(f"\n\n\n{separated_traceback}\n\n")


def set_warnings(debug, ignored_warnings):
    """Define debug type. Can print warnings, ignore them or stop as error

    Args:
        debug (int): If 0, than warnings are ignored, if 1, than warning will be displayed just once, if 2,
            program raise error on warning and stop.
        ignored_warnings (list): List of warnings (any part of inner string) that will be ingored even if debug is set.
    """

    if debug == 1:
        warnings.filterwarnings('once')
    elif debug == 2:
        warnings.filterwarnings('error')
    else:
        warnings.filterwarnings('ignore')

    for i in ignored_warnings:
        warnings.filterwarnings('ignore', message=fr"[\s\S]*{i}*")


def remove_ansi(string):
    """In GUI web page different syntax is necessary than in terminal. This will remove color prefix and replace
    it with html tags.

    Args:
        string (str): String that will be cleaned.

    Returns:
        str: Original string with no color prefix.
    """
    # if not isinstance(string, str):
    #     string = str(string)

    string = string.replace('\033[93m', '<b>')
    string = string.replace('\033[0m', '</b>')

    return string
