import os
from px_secret_sharing.util import prompt_user_for_directory, user_prompt, user_prompt_path
import random
from typing import List, Union

from px_secret_sharing.classes import Piece
from px_secret_sharing.files import list_files_by_extention, read_file
from px_secret_sharing.images import download_stock_images
from px_secret_sharing.steghide import (extract_steghide_image,
                                        filter_images_with_steghide_data)

from .pieces import write_piece
from .shamir import (create_shamir_secret_shares,
                     reconstruct_shamir_secret_shares)
from .summary import write_pieces_summary


class Secret:
    piece_count_min: int
    piece_count_total: int
    piece_count_available: int

    identifier: str

    def __init__(self, minimum: int, total: int, identifier: str):
        self.piece_count_min = minimum
        self.piece_count_total = total
        self.identifier = identifier

    def create(self, user_secret):
        '''
        Split a secret in shares
        '''
        shares = create_shamir_secret_shares(
            user_secret,
            self.identifier,
            self.piece_count_min,
            self.piece_count_total
        )

        return shares

    def reconstruct(self, shares: List[bytes]):
        '''
        Load a secret from shares
        '''
        return reconstruct_shamir_secret_shares(shares)


class SecretSharing:
    working_directory: str

    def __init__(self, working_directory: str):
        self.working_directory = working_directory

    def create(self, secret: Secret, user_secret: str, use_images: bool, image_count: int, summary_dir: Union[str, None], prompt_for_each_location: bool = False) -> List[Piece]:
        '''
        Create a new secret share
        '''
        print('=> Creating a new secret share')

        if not os.path.isdir(self.working_directory):
            os.makedirs(self.working_directory)

        shares = secret.create(user_secret)

        pieces: List[Piece] = []

        for index, share in enumerate(shares, start=1):
            directory = None
            if prompt_for_each_location:
                print('''
Enter the desired path for this piece {}/{}.
The files will be written immideately, so you can change the microSD if necessary.
Ex. /media/secrets
                '''.format(index, len(shares)))
                directory = user_prompt_path()
            else:
                directory = "{}/secret_{}".format(
                    self.working_directory, index
                )

            piece = Piece(
                index,
                directory,
                'note.txt',
                use_images
            )

            if use_images:
                images = download_stock_images(1, directory)
                random_image = random.choice(images)
                write_piece(
                    piece,
                    share,
                    random_image
                )
            else:
                write_piece(
                    piece,
                    share,
                    None
                )

                # piece.delete_piece()

            pieces.append(piece)

        if summary_dir:
            write_pieces_summary(summary_dir, pieces)
        else:
            print('Did not write summary. No path given.')

        return pieces

    def _reconstruct_share(self, piece: Piece) -> Union[bytes, None]:
        print('=> Looking for piece #{} in {}'.format(
            piece.identifier, piece.directory
        ))

        if piece.is_image:
            images = list_files_by_extention(piece.directory, '.jpg')
            images_filtered = filter_images_with_steghide_data(images)
            if len(images_filtered) > 0:
                extract_steghide_image(
                    images_filtered[0], piece.get_piece_path(), '')
            else:
                raise EnvironmentError(
                    'Could not find image with steghide data in {}.'.format(piece.directory))

        if not os.path.isfile(piece.get_piece_path()):
            raise EnvironmentError(
                'Could not find piece data in {}.'.format(
                    piece.get_piece_path())
            )

        share = read_file(piece.get_piece_path(), bytes)
        return share

    def _reconstruct_from_user_input(self, use_images: bool):
        pieces = []
        shares = []

        for number in range(1, 99, 1):
            path = prompt_user_for_directory()

            piece = Piece(
                number,
                path,
                'note.txt',
                use_images
            )
            pieces.append(piece)

            share = self._reconstruct_share(piece)
            if share:
                shares.append(share)
            else:
                print('Piece is invalid or missing: {}'.format(piece.directory))

            if number > 1:
                print('''
We have {} pieces now. Look for more?
                '''.format(len(shares)))
                get_more = user_prompt('Get more piece(s)?')
                if not get_more:
                    return shares, pieces

    def _reconstruct_from_summary(self, summary: List[Piece]) -> List[bytes]:
        shares = []
        piece_count = len(summary)

        print('=> Looking for {} pieces ...'.format(piece_count))

        for piece in summary:
            share = self._reconstruct_share(piece)
            if share:
                shares.append(share)
            else:
                print('Piece is invalid or missing: {}'.format(piece.directory))

        return shares

    def reconstruct(self, summary: Union[List[Piece], None], use_images: bool):
        print('=> Reconstructing an existing secret share')
        shares = None
        if summary:
            shares = self._reconstruct_from_summary(summary)
        else:
            print('No summary selected. Continuing manually.')
            shares, pieces = self._reconstruct_from_user_input(use_images)

        return reconstruct_shamir_secret_shares(shares)
