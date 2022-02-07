from sys import stdout

import px_secret_sharing


def main():
    res = px_secret_sharing.main()
    if res:
        print(res)
    stdout.flush()


if __name__ == '__main__':
    main()
