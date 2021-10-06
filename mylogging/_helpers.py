"""Because of circular import, config cannot import misc, because misc import config
"""

from __future__ import annotations
from typing import Any, Union


def type_and_option_check(
    value: Any,
    variable: Any = "Not defined",
    types: Any = None,
    options: Union[tuple, list] = None,
):
    if isinstance(types, list):
        types = tuple(types)

    if None or (isinstance(types, list) and None in types):
        raise TypeError("None in type checking. None is a value, use type(None).")

    if types and not isinstance(value, types):
        raise TypeError(
            f"Allowed types for variable {variable} are {types}, but you try to set an {type(value)}"
        )

    if options and value not in options:
        raise KeyError(f"New value {value} for variable {variable} is not in allowed options {options}.")
