import os
from typing import Union

from px_secret_sharing.errors import UserAbortException
from px_secret_sharing.steghide import filter_images_with_steghide_data

from .files import list_files_by_extention


def remove_backslash_from_path(path: str):
    if path.endswith('/'):
        return path[:-1]
    else:
        return path


def user_prompt(text: str):
    result = input('{} (yes/no): '.format(text))
    if result.lower() == 'yes':
        return True
    else:
        return False


def user_prompt_image_or_txt():
    print('''
    Are we looking for images note.txt?
    1 - Images
    2 - note.txt
    ''')
    number = int(input('Enter 1 or 2: '))
    if number == 1 or number == 2:
        return number
    else:
        return user_prompt_image_or_txt()


def user_prompt_load_summary_or_prompt():
    print('''
    Would you like to load a summary or get prompted for each piece?
    1 - Prompt
    2 - Summary
    ''')
    number = int(input('Enter 1 or 2: '))
    if number == 1:
        return 'prompt'
    elif number == 2:
        return 'summary'
    else:
        return user_prompt_load_summary_or_prompt()


def user_prompt_create_or_reconstruct():
    print('''
    Would you like to create a new key share, or reconstruct an existing one?
    1 - Create
    2 - Reconstruct
    ''')
    number = int(input('Enter 1 or 2: '))
    if number == 1:
        return 'create'
    elif number == 2:
        return 'reconstruct'
    else:
        return user_prompt_create_or_reconstruct()


def user_prompt_path():
    path = input('Enter path: ')
    if os.path.isdir(path):
        return remove_backslash_from_path(path)
    else:
        print('Path {} does not exist.'.format(path))
        return user_prompt_path()


def user_prompt_file():
    path = input('Enter file path: ')
    if os.path.isfile(path):
        return path
    else:
        print('Path {} does not exist.'.format(path))
        return user_prompt_file()


def _prompt_user_for_directory():
    print('''
    You will be prompted for a path,
    where we expect to find a piece of your secret.

    If you are using the defaults, the folder contains either:
    - a note.txt
    - a bunch of images

    for ex. /media/secret
    ''')
    path = input('Full path: ')
    return path


def _retry_prompt_user_for_directory(overwrite_path: Union[str, None]):
    print('''
    Would you like to retry? Enter 'yes' to retry; anything else to abort.
    ''')
    result = user_prompt('Retry?')
    if result:
        return prompt_user_for_directory(overwrite_path)
    else:
        raise UserAbortException()


def prompt_user_for_directory(overwrite_path: Union[str, None] = None):
    path = None
    if overwrite_path:
        path = overwrite_path
    else:
        path = _prompt_user_for_directory()

        if not os.path.isdir(path):
            print('''The given path does not exist: {}
            Are you sure that it exists?'''.format(path))
            return _retry_prompt_user_for_directory(overwrite_path)

        note_path = "{}/note.txt".format(path)
        if os.path.isfile(note_path):
            print('Given path is correct. Found secret: {}'.format(note_path))
            return path
        else:
            print('Could not find note.txt. Looking for images instead ...')
            images = list_files_by_extention(path, '.jpg')
            if len(images) > 0:
                images_filtered = filter_images_with_steghide_data(images)
                if len(images_filtered) > 0:
                    return path
                else:
                    print('Found {} images but none contain any related data.'.format(
                        len(images)
                    ))
                    return _retry_prompt_user_for_directory(overwrite_path)
            else:
                print('Could not find any images.')
                return _retry_prompt_user_for_directory(overwrite_path)
