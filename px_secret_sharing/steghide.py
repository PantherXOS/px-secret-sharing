import subprocess
from typing import List, Union


def filter_images_with_steghide_data(images: List[str], passphrase: Union[str, None] = None):
    '''
    Filter images with embedded data

    params:
        images: ex.: ['/some_path/image_1.jpg', '/some_path/image_2.jpg']
    '''
    valid_images = []
    for image_path in images:
        command = None
        if passphrase:
            command = "steghide info {} -p {}".format(image_path, passphrase)
        else:
            command = "steghide info {} -p ''".format(image_path)

        result = subprocess.run(
            command, shell=True, capture_output=True
        )

        message = result.stdout.decode()
        if 'embedded file "note.txt"' in message:
            valid_images.append(image_path)

    print('Found {} valid image(s).'.format(len(valid_images)))

    return valid_images


def extract_steghide_image(image_path: str, output_file_path: str, passphrase: Union[str, None] = None):
    '''
    Extract content of specific image to note.txt

    Params:
        image_path: ex.: /some_path/image.jpg
        share_path: ex.: /some_path/note.txt
    '''

    print('=> Extracting from image {}'.format(image_path))
    command = None
    if passphrase:
        command = "steghide extract -sf {} -p {} -xf {}".format(
            image_path, passphrase, output_file_path
        )
    else:
        command = "steghide extract -sf {} -p '' -xf {}".format(
            image_path, output_file_path
        )

    subprocess.run(
        command, shell=True, check=True
    )


def create_steghide_image(image_path: str, data_path: str, passphrase: Union[str, None] = None):
    '''
    Embed share into image

    Params:
        image_path: ex. /some_path/file.jpg
        share_path: ex. /some_path/note.txt
    '''

    print('=> Embedding to image {}'.format(image_path))

    command = None

    if passphrase:
        command = "steghide embed -cf {} -ef {} -p {}".format(
            image_path, data_path, passphrase
        )
    else:
        command = "steghide embed -cf {} -ef {} -p ''".format(
            image_path, data_path
        )

    result = subprocess.run(
        command, shell=True, capture_output=True
    )
    if result.stderr:
        print(result.stderr)
        raise Exception(result.stderr.decode())
