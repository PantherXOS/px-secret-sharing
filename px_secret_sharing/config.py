from appdirs import user_data_dir

WORKING_DIRECTORY = user_data_dir('px-secrets-share')
DEFAULT_SUMMARY = "{}/summary.json".format(WORKING_DIRECTORY)
