# PantherX Secret Sharing

**This is an early preview (pre-v0.0.1).**

The idea behind this is fairly simply.

Let's assume you've setup a secret store like [here](https://wiki.pantherx.org/tomb/#usage). The next challenge would be to securely and redundantly store the key file. This is where `px-secret-sharing` comes in:

1. It will split your key in X (5) parts of which you need Y (3) to recover the key
2. Optionally, for each split, we download a number of random images and embed the part in one

Now you can distribute the X parts.

Recovery works similiarly:

1. Disover images with embedded data and extract
2. If Y or more pieces are available, you will be able to recover the secret

An attacker with less than Y parts won't be able to recover, or even guess the secret more easily than someone with 0 pieces.

## Installation

```
guix package -i px-secret-sharing steghide
```

## Usage Notes

This application is designed to help you easily generate secret shares and optionally keep track of the fact that you have, how many pieces there are, and on what medium they are stored. It should be run on an air-grapped computer.

One could argue that it would make it easier for an intruder to find your keys, if you literally leave a note on your computer that you have X keys, and that they are stored on medium A, B, C (microSD, USB Stick, Mobile Phone, ...). However, I believe:

1. It will encourage you to put more thought into where (or with whom) to keep the pieces
2. It has no impact on the security of the key itself
3. It hopefully lowers the barrier of entry
4. It might give yourself a hint what to look for, if you forget

Let's assume you have 8 pieces of which you need 5. Fast-forward one, two, or three years, you might start to forget where these pieces are, or lose some, without realizing.

Lastly: Consider that you might suffer a sudden loss of memory due to an accident or other reasons, and find youself unable to even remember your name. In this case it might be good, if the pieces are distributed among a set of trusted people that ideally don't know each other.

### Create

```bash
$ px-secret-sharing
Welcome to PantherX Device Identity Service v0.0.1

Working directory: /home/franz/.local/share/px-secrets-share


    Would you like to create a new key share, or reconstruct an existing one?
    1 - Create
    2 - Reconstruct

Enter 1 or 2: 1

Enter the full path under which to find the secret or key that you would like to split.
Ex. /home/franz/tomb_test/secret.tomb.key

Enter file path: /home/franz/tomb_test/secret.tomb.key

These values are currently hard-coded:
- minimum: 3
- total: 5
- identifier: test
- use images: True

=> Creating a new secret share
=> Genering shamir secret shares scheme
=> Downloading stock image to /home/franz/.local/share/px-secrets-share/secret_1/picture_0.jpg
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_1/note.txt
=> Embedding to image /home/franz/.local/share/px-secrets-share/secret_1/picture_0.jpg
=> Downloading stock image to /home/franz/.local/share/px-secrets-share/secret_2/picture_0.jpg
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_2/note.txt
=> Embedding to image /home/franz/.local/share/px-secrets-share/secret_2/picture_0.jpg
=> Downloading stock image to /home/franz/.local/share/px-secrets-share/secret_3/picture_0.jpg
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_3/note.txt
=> Embedding to image /home/franz/.local/share/px-secrets-share/secret_3/picture_0.jpg
=> Downloading stock image to /home/franz/.local/share/px-secrets-share/secret_4/picture_0.jpg
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_4/note.txt
=> Embedding to image /home/franz/.local/share/px-secrets-share/secret_4/picture_0.jpg
=> Downloading stock image to /home/franz/.local/share/px-secrets-share/secret_5/picture_0.jpg
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_5/note.txt
=> Embedding to image /home/franz/.local/share/px-secrets-share/secret_5/picture_0.jpg
=> Saving summary to /home/franz/.local/share/px-secrets-share/summary.json
```

Your secrets will be stored like so:

```bash
ls /home/franz/.local/share/px-secrets-share
secret_1/  secret_2/  secret_3/  secret_4/  secret_5/  summary.json
```

**You should move each `secret_1,2,3,4,5` to a seperate, secure storage and delete `px-secrets-share` afterwards.** Depending on whether you selected images or textfiles, the folders contains either a `note.txt` or `picture_*.jpg`.

### Reconstruct

```bash
$ px-secret-sharing
Working directory: /home/franz/.local/share/px-secrets-share


    Would you like to create a new key share, or reconstruct an existing one?
    1 - Create
    2 - Reconstruct

Enter 1 or 2: 2

    Would you like to load a summary or get prompted for each piece?
    1 - Prompt
    2 - Summary

Enter 1 or 2: 2

Enter the path from which to load the summary (summary.json).
for ex. /home/franz/.local/share/px-secrets-share

Enter path: /home/franz/.local/share/px-secrets-share
=> Loading summary from /home/franz/.local/share/px-secrets-share/summary.json
{'identifier': 1, 'directory': '/home/franz/.local/share/px-secrets-share/secret_1', 'filename': 'note.txt', 'is_image': True}
{'identifier': 2, 'directory': '/home/franz/.local/share/px-secrets-share/secret_2', 'filename': 'note.txt', 'is_image': True}
{'identifier': 3, 'directory': '/home/franz/.local/share/px-secrets-share/secret_3', 'filename': 'note.txt', 'is_image': True}
{'identifier': 4, 'directory': '/home/franz/.local/share/px-secrets-share/secret_4', 'filename': 'note.txt', 'is_image': True}
{'identifier': 5, 'directory': '/home/franz/.local/share/px-secrets-share/secret_5', 'filename': 'note.txt', 'is_image': True}

=> Reconstructing an existing secret share
=> Looking for 5 pieces ...

=> Looking for piece #1 in /home/franz/.local/share/px-secrets-share/secret_1
Found 1 valid image(s).
=> Extracting from image /home/franz/.local/share/px-secrets-share/secret_1/picture_0.jpg
wrote extracted data to "/home/franz/.local/share/px-secrets-share/secret_1/note.txt".
=> Looking for piece #2 in /home/franz/.local/share/px-secrets-share/secret_2
Found 1 valid image(s).
=> Extracting from image /home/franz/.local/share/px-secrets-share/secret_2/picture_0.jpg
wrote extracted data to "/home/franz/.local/share/px-secrets-share/secret_2/note.txt".
=> Looking for piece #3 in /home/franz/.local/share/px-secrets-share/secret_3
Found 1 valid image(s).
=> Extracting from image /home/franz/.local/share/px-secrets-share/secret_3/picture_0.jpg
wrote extracted data to "/home/franz/.local/share/px-secrets-share/secret_3/note.txt".
=> Looking for piece #4 in /home/franz/.local/share/px-secrets-share/secret_4
Found 1 valid image(s).
=> Extracting from image /home/franz/.local/share/px-secrets-share/secret_4/picture_0.jpg
wrote extracted data to "/home/franz/.local/share/px-secrets-share/secret_4/note.txt".
=> Looking for piece #5 in /home/franz/.local/share/px-secrets-share/secret_5
Found 1 valid image(s).
=> Extracting from image /home/franz/.local/share/px-secrets-share/secret_5/picture_0.jpg
wrote extracted data to "/home/franz/.local/share/px-secrets-share/secret_5/note.txt".
=> Reconstructing shamir secret shares scheme

RECONSTRUCTED SECRET

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
```

## Development

```bash
guix environment --pure --ad-hoc python steghide wget
python3 -m venv venv
source venv/bin/activate
pip3 install .
```

### Tests

```bash
$ python3 -m unittest -v

----------------------------------------------------------------------
Ran 5 tests in 22.059s
```

## Credits

This application relies on the MIT-licensed, `tss` library by Sebastien Martini (seb@dbzteam.org). The code is embedded under `px_secret_sharing/tss.py`.
