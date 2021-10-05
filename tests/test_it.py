import sys
from pathlib import Path

import warnings
from io import StringIO

import mypythontools

mypythontools.tests.setup_tests()

import mylogging

from help_file import info_outside, warn_outside, traceback_outside, warn_to_be_filtered
from conftest import logs_stream, setup_tests

setup_tests()


def display_logs(output: str):
    """If want to display check of logs (not tested).
    Also log images from readme and example log are generated here.

    Args:
        output (str, optional): "console" or "example.log". Defaults to "console".
    """
    if output == "console":
        mylogging.config.OUTPUT = "console"

    if output == "example":
        Path("example.log").unlink
        mylogging.config.OUTPUT = "example.log"

    mylogging.warn("I am interesting warning.")

    mylogging.print("No details about me.")

    try:
        print(10 / 0)
    except Exception:
        mylogging.traceback("Maybe try to use something different than 0")

    mylogging.fatal("This is fatal", caption="You can use captions")


def get_stdout_and_stderr(func, args=[], kwargs={}):

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    my_stdout = StringIO()
    my_stderr = StringIO()
    sys.stdout = my_stdout
    sys.stderr = my_stderr

    func(*args, **kwargs)

    output = my_stdout.getvalue() + my_stderr.getvalue() + logs_stream.getvalue()

    logs_stream.truncate(0)

    my_stdout.close()
    my_stderr.close()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    return output


def test_return_str():
    try:
        raise Exception(mylogging.return_str("asdas", caption="User"))
    except Exception:
        # TODO test output
        pass


def test_logs():

    mylogging.config.LEVEL = "DEBUG"
    mylogging.config.FILTER = "always"
    mylogging.config.OUTPUT = "tests/delete.log"

    def check_log():
        with open("tests/delete.log", "r") as log:
            log_content = log.read()
        # Clear content before next run
        # To generate example log comment it out
        open("tests/delete.log", "w").close()

        if log_content:
            return True
        else:
            return False

    mylogging.info(
        "Hessian matrix copmputation failed for example",
        caption="RuntimeError on model x",
    )

    # Info not created
    assert check_log()

    mylogging.warn(
        "Hessian matrix copmputation failed for example",
        caption="RuntimeError on model x",
    )
    mylogging.warn("Second")

    # Warning not created
    assert check_log()

    try:
        print(10 / 0)

    except Exception:
        mylogging.traceback("Maybe try to use something different than 0")

    # Traceback not created
    assert check_log()

    for i in [info_outside, warn_outside, traceback_outside]:
        i("Message")

        # Outside function not working
        assert check_log()

    for handler in mylogging.my_logger.logger.handlers:
        handler.close()

    Path("tests/delete.log").unlink()


def test_warnings_filter():

    ################
    ### Debug = 0 - show not
    ################
    mylogging.config.FILTER = "ignore"

    # Debug 0. Printed, but should not.
    assert not get_stdout_and_stderr(mylogging.warn, ["Asdasd"])

    try:
        print(10 / 0)

    except Exception:
        # Debug = 0 - traceback. Printed, but should not.
        assert not get_stdout_and_stderr(mylogging.traceback, ["Maybe try to use something different than 0"])

    ################
    ### Debug = 1 - show once
    ################
    mylogging.config.FILTER = "once"

    # Debug 1. Not printed, but should.
    assert get_stdout_and_stderr(mylogging.info, ["Hello unique"])
    # Debug 1. Printed, but should not.
    assert not get_stdout_and_stderr(mylogging.info, ["Hello unique"])

    ################
    ### Debug = 2 - show always
    ################

    mylogging.config.FILTER = "always"

    # Debug 2. Not printed, but should.
    assert get_stdout_and_stderr(mylogging.warn, ["Asdasd"])
    # Debug 2. Not printed, but should.
    assert get_stdout_and_stderr(mylogging.warn, ["Asdasd"])

    # Test outer file
    mylogging.config.FILTER = "once"

    # Outside info not working
    assert get_stdout_and_stderr(info_outside, ["Info outside"])


def warn_mode():
    mylogging.config._console_log_or_warn = "warn"

    with warnings.catch_warnings(record=True) as w5:

        warn_outside("Warn outside")
        traceback_outside("Traceback outside")

        # Warn from other file not working
        assert len(w5) == 2


def test_blacklist():

    mylogging.config.BLACKLIST = ["Test blacklist one"]

    assert not get_stdout_and_stderr(mylogging.warn, ["Test blacklist one"])
    assert get_stdout_and_stderr(mylogging.warn, ["Test not blacklisted"])


def test_outer_filters():

    errors = []

    mylogging.config.FILTER = "always"
    warnings.filterwarnings("always")

    ignored_warnings = ["mean of empty slice"]

    # Sometimes only message does not work, then ignore it with class and warning type
    ignored_warnings_class_type = [
        ("TestError", FutureWarning),
    ]

    with warnings.catch_warnings(record=True) as fo:
        mylogging.outer_warnings_filter(ignored_warnings, ignored_warnings_class_type)
        warn_to_be_filtered()

    if fo:
        errors.append("Doesn't filter.")

    with warnings.catch_warnings(record=True) as fo2:
        warn_to_be_filtered()

    if not fo2:
        errors.append("Filter but should not.")

    mylogging.outer_warnings_filter(ignored_warnings, ignored_warnings_class_type)

    with warnings.catch_warnings(record=True) as w6:
        warn_to_be_filtered()

        if w6:
            errors.append("Doesn't filter.")

    mylogging.reset_outer_warnings_filter()

    with warnings.catch_warnings(record=True) as w7:
        warn_to_be_filtered()

    if not w7:
        errors.append("Doesn't filter.")

    assert not errors


def test_warnings_levels():

    errors = []

    # Logging to file is already tested, because level filtering occur before division console or file
    mylogging.config.FILTER = "always"

    all_levels_print_functions = [
        mylogging.debug,
        mylogging.info,
    ]

    all_levels_warnings_functions = [
        mylogging.warn,
        mylogging.error,
        mylogging.critical,
    ]

    message_number_should_pass = 1

    for i in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:

        mylogging.config.LEVEL = i

        with warnings.catch_warnings(record=True) as wl:
            for i in all_levels_warnings_functions:
                i("Message")

        for j in all_levels_print_functions:
            if get_stdout_and_stderr(j, ["Message"]):
                wl.append("Message")

    if not len(wl) != message_number_should_pass:
        errors.append("DEBUG level not correct.")

        message_number_should_pass = message_number_should_pass + 1

    with warnings.catch_warnings(record=True) as wl2:
        mylogging.fatal("This is fatal.")

    if not len(wl2) != message_number_should_pass:
        errors.append("Fatal not working")


# def test_settings():
#     # TODO
#     # Test color and debug
#     pass


def test_readme_configs():
    import mylogging

    mylogging.config.COLORIZE = False  # Turn off colorization on all functions to get rid of weird symbols

    mylogging.info("Not color")


def test_STREAM():
    stream = StringIO()
    mylogging.config.STREAM = stream
    mylogging.warn("Another warning")
    assert stream.getvalue()


def test_redirect_TO_LIST_and_log():
    warnings.filterwarnings("always")

    logs_list = []
    warnings_list = []

    redirect = mylogging.redirect_logs_and_warnings_to_lists(logs_list, warnings_list)

    with warnings.catch_warnings(record=True):  # as warnings_not:
        warnings.warn("Warnings warning.")
        # assert not warnings_not

    assert not get_stdout_and_stderr(mylogging.warn, ["A warning."])

    redirect.close_redirect()

    with warnings.catch_warnings(record=True) as warnings_captured:
        assert get_stdout_and_stderr(mylogging.my_logger.log_and_warn_from_lists, [logs_list, warnings_list])
        # assert warnings_captured

    assert get_stdout_and_stderr(mylogging.warn, ["Should be printed again."])

    with warnings.catch_warnings(record=True) as warnings_again:
        warnings.warn("Warnings warning.")
    assert warnings_again


if __name__ == "__main__":
    # test_return_str()
    # test_logs()
    # test_warnings_filter()
    # test_outer_filters()
    # test_warnings_levels()

    mylogging.config.COLORIZE = True
    mylogging.config.LEVEL = "DEBUG"
    mylogging.config.FILTER = "always"

    display_logs(output="console")
    display_logs(output="example")

    pass
