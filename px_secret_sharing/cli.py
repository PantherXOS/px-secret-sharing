import argparse
import os
import sys

from .classes import RuntimeConfig
from .config import DEFAULT_SUMMARY, WORKING_DIRECTORY
from .util import remove_backslash_from_path


def get_cl_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str, required=True,
                        choices=['create', 'create:prompt', 'reconstruct'],
                        help="""
Primary operations:
(1) 'create' - create and save everything in {} || 
(2) 'create:prompt' - create and get prompted for each location, one by one || 
(3) 'reconstruct' - reconstruct secret from the minimum number of pieces || 

Note: If you supply a summary with '--summary /some-path/summary.json'
your shares should be found automatically assuming all volumes are mounted, otherwise you will be prompted for each loaction.

It's recommended to not suppy a summary and instead write each location one by one. This gives
you time to switch between (for ex.) different microSD cards.
                        """.format(WORKING_DIRECTORY)
                        )
    parser.add_argument("-wd", "--working-directory", type=str, default=WORKING_DIRECTORY,
                        help="Directory in which to store temp files and final summary. Defaults to: {}".format(
                            WORKING_DIRECTORY)
                        )
    parser.add_argument("-min", "--minimum", type=int, default=3,
                        help="CREATE only; Minimum number of pieces required to reconstruct. Defaults to: 3/5"
                        )
    parser.add_argument("-total", "--total", type=int, default=5,
                        help="CREATE only; Total number of pieces to generate. Defaults to: 5"
                        )
    parser.add_argument("-id", "--identifier", type=str, default='note',
                        help="A identifier for this secret. This is only important if you have 2 or more shared secrets. Default: note."
                        )
    parser.add_argument("-img", "--images", type=bool, default=False,
                        help="CREATE only; Whether to conceal the pieces (shares) in images."
                        )
    parser.add_argument("-imgc", "--image_count", type=str, default=1,
                        help="CREATE only; How many stock images you would like to download to each folder. Default: 1"
                        )
    parser.add_argument("-s", "--secret", type=str, default=None,
                        help="""CREATE: The file that contains the secret to be split and shared. Ex. /some-path/secret.tomb.key
RECONSTRUCT: The file the secret should be written to. If this is ommited, it will be written to stdout (prints in command line).
"""
                        )
    parser.add_argument("-sum", "--summary", type=str, default=None,
                        help="RECONSTRUCT only; The file that contains the summary of an existing share. Defaults to: {}.".format(
                            DEFAULT_SUMMARY)
                        )

    args = parser.parse_args()
    operation = args.operation.lower()
    working_directory = remove_backslash_from_path(args.working_directory)
    minimum_pieces = args.minimum
    total_pieces = args.total
    identifier = args.identifier
    use_images = args.images
    image_count = args.image_count
    user_secret_file_path = args.secret
    summary_file_path = args.summary

    if operation == 'create' or operation == 'create:prompt':
        if not user_secret_file_path:
            print(
                'You need to indicate where to find your secret: --secret /some-path/secret.tomb.key'
            )
            sys.exit(1)

        if not os.path.isfile(user_secret_file_path):
            print(
                'Could not find secret at {}'.format(user_secret_file_path)
            )
            sys.exit(1)

    if operation == 'reconstruct':
        if summary_file_path:
            if not os.path.isfile(summary_file_path):
                print(
                    'Could not find summary at {}'.format(summary_file_path)
                )
                sys.exit(1)
            if not summary_file_path.endswith('.json'):
                print(
                    'Expecting to find a summary in JSON format (.json).'
                )
                sys.exit(1)

    config = RuntimeConfig(
        operation,
        working_directory,
        minimum_pieces,
        total_pieces,
        identifier,
        use_images,
        image_count,
        None,
        user_secret_file_path,
        summary_file_path
    )

    return config
