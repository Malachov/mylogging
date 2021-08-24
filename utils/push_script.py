import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\Malac\ownCloud\Github\mypythontools")


import mypythontools

# mypythontools imports mylogging, so tests can fail. Turn off and run manually...
if __name__ == "__main__":
    mypythontools.utils.push_pipeline(
        test=True, test_options={"requirements": "requirements.txt", "verbose": True}, deploy=False
    )

    # mypythontools.paths.set_paths()
    # mypythontools.tests.run_tests(requirements="requirements.txt", verbose=True)
