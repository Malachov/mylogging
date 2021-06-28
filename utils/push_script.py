import mypythontools

# mypythontools imports mylogging, so tests can fail. Turn off arun manually...
if __name__ == "__main__":
    mypythontools.utils.push_pipeline(tests=False, deploy=True)
