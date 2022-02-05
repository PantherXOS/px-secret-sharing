import os
from dataclasses import dataclass


@dataclass
class Piece:
    '''
    This represents one piece of Shamir's secret sharing scheme

    identifier: the identifier of the piece; ex. 1
    directory: the full path to the folder that contains the piece
    filename: the filename of the actual piece; ex. note.txt
    '''
    identifier: int
    directory: str
    filename: str
    is_image: bool

    def __init__(self, identifier: int, directory: str, filename: str, is_image: bool):
        self.identifier = identifier
        self.directory = directory
        self.filename = filename
        self.is_image = is_image

    def get_piece_path(self):
        return "{}/{}".format(self.directory, self.filename)

    def delete_piece(self):
        '''
        Deletes the textfile
        This is usually done when the piece is an image (is_image)
        '''
        if os.path.isfile(self.get_piece_path()):
            os.unlink(self.get_piece_path())
        else:
            print("File {} already deleted.".format(self.get_piece_path()))
