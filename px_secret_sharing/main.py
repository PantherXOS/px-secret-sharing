from typing import Union

import pkg_resources

from px_secret_sharing.classes import RuntimeConfig
from px_secret_sharing.cli import get_cl_arguments
from px_secret_sharing.summary import load_pieces_summary

from .files import read_file, write_file
from .secret_sharing import Secret, SecretSharing

version = pkg_resources.require("px_secret_sharing")[0].version


def main(test_config: Union[RuntimeConfig, None] = None):
    print('Welcome to PantherX Secret Sharing v{}'.format(version))

    config = None
    if test_config:
        config = test_config
    else:
        config = get_cl_arguments()

    print('''
Working directory: {}
    '''.format(config.working_directory))

    if config.operation == 'create' or config.operation == 'create:prompt':

        user_secret = None
        if config.user_secret:
            user_secret = config.user_secret
        elif config.user_secret_file_path:
            user_secret = read_file(config.user_secret_file_path)
        else:
            raise EnvironmentError('Cannot proceed without user secret.')

        secret_sharing = SecretSharing(
            config.working_directory, config.identifier
        )

        secret = Secret(
            minimum=config.minimum_pieces,
            total=config.total_pieces,
            identifier=config.identifier
        )

        prompt_for_each_location = False
        if config.operation == 'create:prompt':
            prompt_for_each_location = True
        pieces = secret_sharing.create(
            secret=secret,
            user_secret=user_secret,
            use_images=config.use_images,
            image_count=config.image_count,
            summary_dir=config.working_directory,
            prompt_for_each_location=prompt_for_each_location
        )

        print('''
Now that your secret has been split in {} pieces, you should:
1. Distribute these pieces across various places
2. Delete each secret after it has been relocated
3. Optionally, delete the whole folder {}

Make sure that two secrets are never on the same device, or same physical location
        '''.format(len(pieces), config.working_directory))
    elif config.operation == 'reconstruct':
        secret = None
        if config.summary_file_path:
            summary = load_pieces_summary(config.summary_file_path)
            secret_sharing = SecretSharing(
                config.working_directory, config.identifier)
            secret = secret_sharing.reconstruct(summary, config.use_images)

        else:
            secret_sharing = SecretSharing(
                config.working_directory, config.identifier)
            secret = secret_sharing.reconstruct(None, config.use_images)

        if secret and config.user_secret_file_path:
            write_file(config.user_secret_file_path, secret)
        elif secret:
            return secret


if __name__ == '__main__':
    main()
