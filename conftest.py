from io import StringIO
import pytest

from pathlib import Path
import sys

sys.path.insert(0, Path(__file__).parent)
import mylogging

import mypythontools

mypythontools.tests.setup_tests()


logs_stream = StringIO()


@pytest.fixture(autouse=True)
def setup_tests_fixture():
    setup_tests()


def setup_tests():
    mylogging.config.LEVEL = "INFO"
    mylogging.config._console_log_or_warn = "log"
    mylogging.config.STREAM = logs_stream
    mylogging.config.OUTPUT = "console"
    mylogging.config.FILTER = "always"
    logs_stream.truncate(0)