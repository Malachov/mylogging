"""Tests for mylogging package. Usually runs from IDE, where configured via conftest."""
import sys
from pathlib import Path

# mylogging is used in mypythontools, so need to be imported separately, not in setup_tests()
sys.path.insert(0, (Path.cwd().parent / "mypythontools").as_posix())
sys.path.insert(0, Path(__file__).parents[1].as_posix())
from conftest import setup_tests

setup_tests()


# TODO delete me
import sys
from pathlib import Path

import mypythontools

from mylogging.colors import colorize_traceback
from mylogging import format_str

import mylogging


mylogging.config.colorize = True

import sys

# print(sys.tracebacklimit)

mylogging.my_traceback.enhance_excepthook()


def function_one():
    try:

        def aho():
            raise TypeError("Example of colored traceback exception.")

        aho()
    except Exception:
        mylogging.traceback(remove_frame_by_line_str="asdsad")


def function_two():
    function_one()


function_two()


# def test_raise_with_traceback():
#     # try:
#     #     mylogging.raise_with(TypeError, "Yes")
#     # except TypeError as e:
#     #     print(e)
#     def ahoj():
#         # raise TypeError.with_traceback(mylogging.raise_with_traceback(TypeError, "asd"))
#         mylogging.raise_with_traceback(TypeError, "asd")

#     #     mylogging.raise_with_traceback(TypeError, "Yes")

#     ahoj()
