"""pytest file built from C:/Users/Malac/ownCloud/Github/mylogging/README.md"""
import pytest

from phmdoctest.fixture import managenamespace


@pytest.fixture(scope="module")
def _phm_setup_teardown(managenamespace):
    # setup code line 59.
    import mylogging

    mylogging.config.LEVEL = "WARNING"
    mylogging.warn("I am interesting warning.")

    managenamespace(operation="update", additions=locals())
    yield
    # <teardown code here>

    managenamespace(operation="clear")


pytestmark = pytest.mark.usefixtures("_phm_setup_teardown")


def test_code_68():
    try:
        print(10 / 0)

    except ZeroDivisionError:
        mylogging.traceback("Maybe try to use something different than 0.")

    mylogging.fatal("This is fatal", caption="You can use captions")

    # Caution- no assertions.


def test_code_80():
    mylogging.print("No details about me.")

    # Caution- no assertions.


@pytest.mark.skip()
def test_code_88():
    raise ModuleNotFoundError(mylogging.return_str("Try pip install...", caption="Library not installed error"))

    # Caution- no assertions.


def test_code_104():
    ignored_warnings = ["mean of empty slice"]
    ignored_warnings_class_type = [
        ("TestError", FutureWarning),
    ]

    mylogging.outer_warnings_filter(ignored_warnings, ignored_warnings_class_type)

    mylogging.reset_outer_warnings_filter()

    # Caution- no assertions.


def test_code_165():
    logs_list = []
    warnings_list = []

    logs_redirect = mylogging.redirect_logs_and_warnings_to_lists(logs_list, warnings_list)

    logs_redirect.close_redirect()

    mylogging.my_logger.log_and_warn_from_lists(logs_list, warnings_list)

    # Caution- no assertions.
