"""pytest file built from c:/Users/Turtor/ownCloud/Github/mylogging/README.md"""
import pytest

from phmdoctest.fixture import managenamespace


@pytest.fixture(scope="module")
def _phm_setup_teardown(managenamespace):
    # setup code line 59.
    import mylogging

    mylogging.config.level = "WARNING"
    mylogging.warn("I am interesting warning.")

    managenamespace(operation="update", additions=locals())
    yield
    # <teardown code here>

    managenamespace(operation="clear")


pytestmark = pytest.mark.usefixtures("_phm_setup_teardown")


def test_code_70():
    try:
        print(10 / 0)
    except ZeroDivisionError:
        mylogging.traceback("Maybe try to use something different than 0.")

    # Caution- no assertions.


def test_code_79():
    mylogging.my_traceback.enhance_excepthook_reset()

    # Caution- no assertions.


def test_code_88():
    mylogging.print("No details about me.")

    # Caution- no assertions.


def test_code_96():
    import warnings

    ignored_warnings = ["mean of empty slice"]
    ignored_warnings_class_type = [
        ("TestError", FutureWarning),
    ]

    mylogging.my_warnings.filter_always(ignored_warnings, ignored_warnings_class_type)

    warnings.warn("mean of empty slice")  # No output

    mylogging.my_warnings.reset_filter_always()

    # Caution- no assertions.


def test_code_161():
    logs_list = []
    warnings_list = []

    logs_redirect = mylogging.misc.redirect_logs_and_warnings(logs_list, warnings_list)

    logs_redirect.close_redirect()

    mylogging.misc.log_and_warn_from_lists(logs_list, warnings_list)

    # Caution- no assertions.
