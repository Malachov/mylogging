import mypythontools

# mypythontools imports mylogging, so tests can fail. Turn off and run manually...
if __name__ == "__main__":
    mypythontools.utils.push_pipeline(test=True, deploy=True)
