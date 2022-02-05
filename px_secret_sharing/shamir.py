from typing import List

from . import tss


def create_shamir_secret_shares(user_secret: str, user_secret_identifier: str, pieces_minimum: int, pieces_total: int):
    print('=> Splitting secret into {} pieces (Shamir Secret Shares Scheme)'.format(
        pieces_total
    ))
    return tss.share_secret(
        pieces_minimum,
        pieces_total,
        user_secret,
        user_secret_identifier,
        tss.Hash.SHA256
    )


def reconstruct_shamir_secret_shares(shares: List[bytes]):
    print('=> Reconstructing from {} pieces (Shamir Secret Shares Scheme)'.format(
        len(shares)
    ))
    try:
        secret = tss.reconstruct_secret(shares)
        return secret.decode()
    except tss.TSSError as err:
        print(err)
        return
