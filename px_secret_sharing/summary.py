import json
from typing import List

from .classes import Piece
from .files import read_file, write_file
from .util import (prompt_user_for_directory, user_prompt,
                   user_prompt_image_or_txt)


def assemble_summary_from_user_input():
    pieces = []

    images_or_note = user_prompt_image_or_txt()
    images = images_or_note == 1

    for number in range(99):
        path = prompt_user_for_directory()

        piece = Piece(
            number,
            path,
            'note.txt',
            images
        )
        pieces.append(piece)
        if number > 0:
            print('''
            We have {} piece(s). Should we look for more?
            '''.format(len(pieces)))
            get_more = user_prompt('Get more pieces?')
            if get_more:
                continue
            else:
                return pieces


def load_pieces_summary(directory: str) -> List[Piece]:
    path = "{}/summary.json".format(directory)
    print('=> Loading summary from {}'.format(path))
    summary_content = read_file(path)
    summary = json.loads(summary_content)

    pieces = []
    for item in summary:
        print(item)
        piece = Piece(
            item['identifier'],
            item['directory'],
            item['filename'],
            item['is_image']
        )
        pieces.append(piece)

    return pieces


def write_pieces_summary(directory: str, pieces: List[Piece]):
    '''
    This summary is entirely optional and is designed to keep track of pieces.
    If you do not keep a summary, assembling the pieces will be more verbose
    '''
    path = "{}/summary.json".format(directory)
    print('=> Saving summary to {}'.format(path))
    pieces_dict = []
    for piece in pieces:
        pieces_dict.append(piece.__dict__)
    summary_content = json.dumps(pieces_dict)
    write_file(path, summary_content)