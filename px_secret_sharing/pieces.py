import os
from typing import Union

from px_secret_sharing.classes import Piece

from .files import list_files_by_extention, read_file, write_file
from .steghide import (create_steghide_image, extract_steghide_image,
                       filter_images_with_steghide_data)


def write_piece(piece: Piece, content: bytes, image_path: Union[str, None], passphrase: Union[str, None] = None):
    '''
    Write a new piece to textfile or image

    Params:
        directory: the full path to the directory where to store textfile or image
        output_file_path: full path to the textfile with the piece
        content: the actual piece to be written to output_file_path
        write_to_image: embed the piece in an image; delete the textfile
        image_path: path of the image to use (this will modify the original)
        passprase: optional passphrase to secure the image

        We default to '' for the passphrase, because it might just be overkill to do this ...
    '''
    if not os.path.isdir(piece.directory):
        os.makedirs(piece.directory)

    print('=> Creating piece at {}'.format(piece.get_piece_path()))

    write_file(piece.get_piece_path(), content)

    if piece.is_image:
        if not image_path:
            raise ValueError(
                'Tried to write piece to image, but did not receive image path.'
            )
        create_steghide_image(image_path, piece.get_piece_path(), passphrase)
        piece.delete_piece()


def read_piece(directory: str, output_file_path: str, load_from_image: bool = False, passphrase: str = '', delete_output_immideately: bool = True):
    '''
    Read a piece from text file or image

    params:
        directory: the full path of the directory that contains the piece
        output_file_path: the full path to the piece (if image, this is where we write the piece)
        load_from_image: extract the piece from the image first
        passphrase: optional passphrase with which the image may be secured
        delete_output_immideately: in case we load the piece from the image, we should delete the textfile after reading
    '''
    if load_from_image:
        images = list_files_by_extention(directory, '.jpg')
        images_with_data = filter_images_with_steghide_data(images)
        # we default to extract the first image
        if len(images_with_data) > 0:
            extract_steghide_image(
                images_with_data[0], output_file_path, passphrase
            )
        else:
            raise Exception(
                'No steghide image found in {}.'.format(directory)
            )

    if not os.path.isfile(output_file_path):
        raise Exception('No file found at {}.'.format(output_file_path))

    piece = read_file(output_file_path, bytes)
    if load_from_image and delete_output_immideately:
        os.unlink(output_file_path)

    return piece
