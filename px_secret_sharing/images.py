import os
import random
import subprocess
from typing import List

from px_secret_sharing.files import list_files_by_extention


def get_random_image(directory: str):
    '''
    Get random image from a folder

    Params:
        dir: ex. /some_path
    '''
    images = list_files_by_extention(directory, '.jpg')
    image = random.choice(images)
    return image


def download_stock_images(count: int, directory: str) -> List[str]:
    '''
    Download a number of images to share folder and embed share in one of them.
    The share file at share_path should be deleted after this.

    Params:
        count: number of images to download
        dir: the image destination
    '''
    if not os.path.isdir(directory):
        os.makedirs(directory)

    images = []
    for number in range(count):
        image_path = "{}/picture_{}.jpg".format(directory, number)
        print('=> Downloading stock image to {}'.format(image_path))
        subprocess.run(
            'wget -q -O {} https://unsplash.it/1920/1080/?random'.format(
                image_path), shell=True
        )
        images.append(image_path)

    return images
