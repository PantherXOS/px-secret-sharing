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

## Usage

```bash
usage: px-secret-sharing [-h]
	-o {create, create:prompt, reconstruct}
	[-wd WORKING_DIRECTORY]
	[-min MINIMUM]
	[-total TOTAL]
	[-id IDENTIFIER]
	[-img IMAGES]
	[-imgc IMAGE_COUNT]
	[-s SECRET]
	[-sum SUMMARY]
```

There's two primary options:

1. Create
   - `create`: To create a new share and save all pieces to the working directory
   - `create:prompt`: Create a new share but provide location of pieces one by one
2. Reconstruct
   - From Summary: Load `summary.json` to collect pieces automatically
   - From Prompt: You will be prompted for the location of each pieces

Reconstruction from prompt is usually the most reliable. The application will prompt you for the path of each secret, and you may switch drives between prompts (unplug SD card; plugin another).

### 1. Create

With defaults:

```bash
px-secret-sharing -o create --secret /home/franz/tomb_test/secret.tomb.key

# To get prrompted for each location:
px-secret-sharing -o create:prompt --secret /home/franz/tomb_test/secret.tomb.key
```

With defaults but embed pieces to images instead of .txt files. The images will be downloaded from `unsplash.it`.:

```bash
px-secret-sharing -o CREATE -img True --secret /home/franz/tomb_test/secret.tomb.key
```

All options:

```bash
px-secret-sharing -o [create,create:prompt]
```

**Example**

```bash
$ px-secret-sharing -o CREATE --secret /home/franz/tomb_test/secret.tomb.key
Welcome to PantherX Secret Sharing v0.0.0

Working directory: /home/franz/.local/share/px-secrets-share

=> Creating a new secret share
=> Genering shamir secret shares scheme
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_1/note.txt
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_2/note.txt
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_3/note.txt
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_4/note.txt
=> Creating piece at /home/franz/.local/share/px-secrets-share/secret_5/note.txt
=> Saving summary to /home/franz/.local/share/px-secrets-share/summary.json
```

Your secrets will be stored like so:

```bash
ls /home/franz/.local/share/px-secrets-share
secret_1/  secret_2/  secret_3/  secret_4/  secret_5/  summary.json
```

**You should move each `secret_1,2,3,4,5` to a seperate, secure storage and ideally `~.local/share/px-secrets-share/px-secrets-share` afterwards.** Depending on whether you selected images or textfiles, the folders contains either a `note.txt` or `picture_*.jpg`.

### 2. Reconstruct

#### From Summary

```bash
$ px-secret-sharing -o RECONSTRUCT -sum /home/franz/.local/share/px-secrets-share/summary.json
Welcome to PantherX Secret Sharing v0.0.0

Working directory: /home/franz/.local/share/px-secrets-share

=> Loading summary from /home/franz/.local/share/px-secrets-share/summary.json
{'identifier': 1, 'directory': '/home/franz/.local/share/px-secrets-share/secret_1', 'filename': 'note.txt', 'is_image': False}
{'identifier': 2, 'directory': '/home/franz/.local/share/px-secrets-share/secret_2', 'filename': 'note.txt', 'is_image': False}
{'identifier': 3, 'directory': '/home/franz/.local/share/px-secrets-share/secret_3', 'filename': 'note.txt', 'is_image': False}
{'identifier': 4, 'directory': '/home/franz/.local/share/px-secrets-share/secret_4', 'filename': 'note.txt', 'is_image': False}
{'identifier': 5, 'directory': '/home/franz/.local/share/px-secrets-share/secret_5', 'filename': 'note.txt', 'is_image': False}
=> Reconstructing an existing secret share
=> Looking for 5 pieces ...
=> Looking for piece #1 in /home/franz/.local/share/px-secrets-share/secret_1
=> Looking for piece #2 in /home/franz/.local/share/px-secrets-share/secret_2
=> Looking for piece #3 in /home/franz/.local/share/px-secrets-share/secret_3
=> Looking for piece #4 in /home/franz/.local/share/px-secrets-share/secret_4
=> Looking for piece #5 in /home/franz/.local/share/px-secrets-share/secret_5
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

#### From Prompt

```bash
$ px-secret-sharing -o RECONSTRUCT
Welcome to PantherX Secret Sharing v0.0.0

Working directory: /home/franz/.local/share/px-secrets-share

=> Reconstructing an existing secret share
No summary selected. Continuing manually.

    Are we looking for images note.txt?
    1 - Images
    2 - note.txt

Enter 1 or 2: 2

    You will be prompted for a path,
    where we expect to find a piece of your secret.

    If you are using the defaults, the folder contains either:
    - a note.txt
    - a bunch of images

    for ex. /media/secret

Full path: /home/franz/.local/share/px-secrets-share/secret_1
Given path is correct. Found secret: /home/franz/.local/share/px-secrets-share/secret_1/note.txt

    You will be prompted for a path,
    where we expect to find a piece of your secret.

    If you are using the defaults, the folder contains either:
    - a note.txt
    - a bunch of images

    for ex. /media/secret

Full path: /home/franz/.local/share/px-secrets-share/secret_2
Given path is correct. Found secret: /home/franz/.local/share/px-secrets-share/secret_2/note.txt

    We have 2 piece(s). Should we look for more?

Get more pieces? (yes/no): yes

    You will be prompted for a path,
    where we expect to find a piece of your secret.

    If you are using the defaults, the folder contains either:
    - a note.txt
    - a bunch of images

    for ex. /media/secret

Full path: /home/franz/.local/share/px-secrets-share/secret_3
Given path is correct. Found secret: /home/franz/.local/share/px-secrets-share/secret_3/note.txt

    We have 3 piece(s). Should we look for more?

Get more pieces? (yes/no): no
=> Looking for 3 pieces ...
=> Looking for piece #0 in /home/franz/.local/share/px-secrets-share/secret_1
=> Looking for piece #1 in /home/franz/.local/share/px-secrets-share/secret_2
=> Looking for piece #2 in /home/franz/.local/share/px-secrets-share/secret_3
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

## Usage Notes

This application is designed to help you easily generate secret shares and optionally keep track of the fact that you have, how many pieces there are, and on what medium they are stored. It should be run on an air-grapped computer.

One could argue that it would make it easier for an intruder to find your keys, if you literally leave a note on your computer that you have X keys, and that they are stored on medium A, B, C (microSD, USB Stick, Mobile Phone, ...). However, I believe:

1. It will encourage you to put more thought into where (or with whom) to keep the pieces
2. It has no impact on the security of the key itself
3. It hopefully lowers the barrier of entry
4. It might give yourself a hint what to look for, if you forget

Let's assume you have 8 pieces of which you need 5. Fast-forward one, two, or three years, you might start to forget where these pieces are, or lose some, without realizing.

Lastly: Consider that you might suffer a sudden loss of memory due to an accident or other reasons, and find youself unable to even remember your name. In this case it might be good, if the pieces are distributed among a set of trusted people that ideally don't know each other.

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

The source code can be found on [github.com/seb-m/tss](https://github.com/seb-m/tss)
