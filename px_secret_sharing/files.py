import os
import shutil
from typing import Union


def list_files(dir: str):
    return os.listdir(dir)


def list_files_by_extention(dir: str, file_extention: str):
    '''
    Get a list of files by file name

    Params:
        dir: ex. /some_path
        file_type: ex. '.jpg'
    '''
    files = list_files(dir)
    files_filtered = []
    for file in files:
        if file.endswith(file_extention):
            image_path = "{}/{}".format(dir, file)
            files_filtered.append(image_path)
    return files_filtered


def copy_file(file_path: str, directory: str):
    '''
    Copy a file from A to B

    Params:
        file_path: ex. /some_path/file.jpg
        dir: ex. /some_other_part
    '''
    shutil.copy(file_path, directory)


def write_file(file_path: str, content: Union[str, bytes]):
    mode = 'w'
    if type(content) is bytes:
        mode = 'wb'

    with open(file_path, mode) as writer:
        writer.write(content)


def read_file(file_path: str, data_type: type = str):
    mode = 'r'
    if data_type is bytes:
        mode = 'rb'
    with open(file_path, mode) as reader:
        return reader.read()
