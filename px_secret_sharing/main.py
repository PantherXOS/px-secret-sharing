from typing import Union

import pkg_resources

from px_secret_sharing.config import WORKING_DIRECTORY
from px_secret_sharing.summary import load_pieces_summary
from px_secret_sharing.util import (user_prompt_create_or_reconstruct,
                                    user_prompt_file,
                                    user_prompt_load_summary_or_prompt,
                                    user_prompt_path)

from .files import read_file
from .secret_sharing import Secret, SecretSharing

version = pkg_resources.require("px_secret_sharing")[0].version


def main(test_config: Union[dict, None] = None):
    print('Welcome to PantherX Device Identity Service v{}'.format(version))

    working_directory = WORKING_DIRECTORY
    if test_config:
        working_directory = test_config['working_directory']

    print('''
Working directory: {}
    '''.format(working_directory))

    method = None
    if test_config:
        method = test_config['method']
    else:
        method = user_prompt_create_or_reconstruct()

    if method == 'create':

        secret_sharing = SecretSharing(working_directory)
        if test_config:
            secret = Secret(
                minimum=test_config['min'],
                total=test_config['total'],
                identifier=test_config['identifier']
            )
            secret_sharing.create(
                secret=secret,
                user_secret=test_config['user_secret'],
                use_images=test_config['use_images'],
                summary_dir=test_config['working_directory']
            )
        else:
            print('''
Enter the full path under which to find the secret or key that you would like to split.
Ex. /home/franz/tomb_test/secret.tomb.key
            ''')
            path = user_prompt_file()
            user_secret = read_file(path)

            print('''
These values are currently hard-coded:
- minimum: 3
- total: 5
- identifier: test
- use images: True
            ''')

            secret = Secret(
                minimum=3,
                total=5,
                identifier='test'
            )
            secret_sharing.create(
                secret=secret,
                user_secret=user_secret,
                use_images=True,
                summary_dir=working_directory
            )

    else:
        reconstruction_method = None
        if test_config:
            reconstruction_method = test_config['reconstruction_method']
        else:
            reconstruction_method = user_prompt_load_summary_or_prompt()

        if reconstruction_method == 'prompt':
            secret_sharing = SecretSharing(working_directory)
            secret = secret_sharing.reconstruct(None)
            print('RECONSTRUCTED SECRET')
            print(secret)
        else:
            print('''
Enter the path from which to load the summary (summary.json).
for ex. {}
            '''.format(WORKING_DIRECTORY))
            path = None
            if test_config:
                path = test_config['working_directory']
            else:
                path = user_prompt_path()
            summary = load_pieces_summary(path)

            secret_sharing = SecretSharing(working_directory)
            secret = secret_sharing.reconstruct(summary)

            print('RECONSTRUCTED SECRET')
            print(secret)


if __name__ == '__main__':
    main()
