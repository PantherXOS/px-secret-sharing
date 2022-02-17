import os
from px_secret_sharing.classes import RuntimeConfig
import shutil
import unittest

from px_secret_sharing import Secret, SecretSharing
from px_secret_sharing.files import list_files_by_extention
from px_secret_sharing.main import main
from px_secret_sharing.steghide import filter_images_with_steghide_data
from px_secret_sharing.summary import load_pieces_summary

file_dir = '/tmp/px_secrets_share_test_general'

user_secret = '''
jA0ECQMCMCn5czbQJfr10ukBUj7rEDEBEnrzqLePghZl5VE4L04Sc9seJMmUeon5
QEoYMUGU7zpBhPbXkVVzATgzTq0pU4Rg6NQ78tbs0lb5YE6oQqQc+vDeWDfe+EoO
Y4zylb9GjVb4liCVwmfnhqcfwMOpD8AxyPSOgBmetNHwV9/n58mcp+efN3nUc4ga
nrEu687MpeSZsJ4Wl31X/66WHrO+TfKxa4DbV9ckUSQ6+wnjsj2DyuvWySBMMKfj
ZnRb7uqRoo/BnWFGxxA27dCxKgF0p/2AKiWhOgn1Ex1X6jAaU6haiHIogvbpkHcd
xNF7azv0ahm849UMrUcM/IK2qc+Il++6JCM/OZSh0WlqEO2PHxdRXANQJgmZmu5A
HmjMhROlmNX8BfmhaqE1DbjDnyfJycQ/tUvQ6K3w2YWrPzOPI9lzwpsHVYLWHoB2
W9hcUH/1+E1uIFzvtUoy8pYp644vfdPI/b7FnWaC8doKioOHIWb8ndIgu91lsT9j
+C6A7xMHMV1K6qsxIYUMrAOAQgfjK3APhSabTS8J8IC0L94p8trFaavCTejCdx7W
JplWYGvYlbvcqn2pwADXQNkLpbFw4CgHvoOHNA5xtp6MtX+a+2YkTDLztQzVf3vK
wgqqSktjnQbK4uNda8V8QZ7RUDCCx4JWpPCtJ8KqWFiS83q9ZXv1OsjzE+PIBpaA
OziWiJ05XyQ29ErIt18Od4A4KR7fXBotmOKyhxRFZP/yomGbsp17MXRv61Dl4x83
5T9kmFe5D8nuxQ==
=L7Us
'''
user_secret_identifier = 'test_01'


class TestGeneral(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(file_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(file_dir)

    def test_main_create(self):
        # (1) Create secret
        main(RuntimeConfig(
            operation='create',
            working_directory=file_dir,
            minimum_pieces=3,
            total_pieces=5,
            identifier='test',
            use_images=False,
            image_count=0,
            user_secret=user_secret,
            user_secret_file_path=None,
            summary_file_path=None
        ))

    def test_main_reconstruct(self):
        # (1) Create secret
        main(RuntimeConfig(
            operation='create',
            working_directory=file_dir,
            minimum_pieces=3,
            total_pieces=5,
            identifier='test',
            use_images=False,
            image_count=0,
            user_secret=user_secret,
            user_secret_file_path=None,
            summary_file_path=None
        ))

        main(RuntimeConfig(
            operation='reconstruct',
            working_directory=file_dir,
            minimum_pieces=3,
            total_pieces=5,
            identifier='test',
            use_images=False,
            image_count=0,
            user_secret=user_secret,
            user_secret_file_path=None,
            summary_file_path='{}/summary.json'.format(file_dir)
        ))

    def test_with_textfiles(self):
        # (1) Create secret
        secret_sharing = SecretSharing(file_dir, 'test')
        secret = Secret(5, 8, 'test')

        pieces = secret_sharing.create(
            secret,
            user_secret,
            False,
            0,
            None
        )

        self.assertEqual(len(pieces), 8)
        for piece in pieces:
            exists = os.path.isfile(piece.get_piece_path())
            self.assertTrue(exists)

        # (2) Recover secret
        recovered_secret = secret_sharing.reconstruct(pieces, False)
        self.assertEqual(user_secret, recovered_secret)

    def test_with_textfiles_load_summary(self):
        # (1) Create secret
        secret_sharing = SecretSharing(file_dir, 'test')
        secret = Secret(5, 8, 'test')

        pieces = secret_sharing.create(
            secret,
            user_secret,
            False,
            0,
            file_dir
        )

        self.assertEqual(len(pieces), 8)
        for piece in pieces:
            exists = os.path.isfile(piece.get_piece_path())
            self.assertTrue(exists)

        # (2) Recover secret
        summary = load_pieces_summary('{}/summary.json'.format(file_dir))
        recovered_secret = secret_sharing.reconstruct(summary, False)
        self.assertEqual(user_secret, recovered_secret)

    def test_with_images(self):
        # (1) Create secret
        secret_sharing = SecretSharing(file_dir, 'test')
        secret = Secret(2, 3, 'test')

        pieces = secret_sharing.create(
            secret,
            user_secret,
            True,
            1,
            None
        )

        self.assertEqual(len(pieces), 3)
        for piece in pieces:
            # when using images, the txt file should be deleted
            exists = os.path.isfile(piece.get_piece_path())
            self.assertFalse(exists)
            images = list_files_by_extention(piece.directory, '.jpg')
            images_filtered = filter_images_with_steghide_data(images)
            self.assertEqual(len(images_filtered), 1)

        # (2) Recover secret
        recovered_secret = secret_sharing.reconstruct(pieces, True)
        self.assertEqual(user_secret, recovered_secret)

    def test_manual(self):
        # (1) Create secret
        secret_sharing = SecretSharing(file_dir, 'test')
        secret = Secret(2, 3, 'test')

        pieces = secret_sharing.create(
            secret,
            user_secret,
            False,
            2,
            None
        )

        self.assertEqual(len(pieces), 3)
        for piece in pieces:
            exists = os.path.isfile(piece.get_piece_path())
            self.assertTrue(exists)

        # (2) Recover secret
        recovered_secret = secret_sharing.reconstruct(None, False)
        self.assertEqual(user_secret, recovered_secret)

    def test_manual_with_images(self):
        # (1) Create secret
        secret_sharing = SecretSharing(file_dir, 'test')
        secret = Secret(2, 3, 'test')

        pieces = secret_sharing.create(
            secret,
            user_secret,
            True,
            2,
            None
        )

        self.assertEqual(len(pieces), 3)
        for piece in pieces:
            # when using images, the txt file should be deleted
            exists = os.path.isfile(piece.get_piece_path())
            self.assertFalse(exists)
            images = list_files_by_extention(piece.directory, '.jpg')
            images_filtered = filter_images_with_steghide_data(images)
            self.assertEqual(len(images_filtered), 1)

        # (2) Recover secret
        recovered_secret = secret_sharing.reconstruct(None, True)
        self.assertEqual(user_secret, recovered_secret)
