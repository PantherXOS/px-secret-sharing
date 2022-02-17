import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'px-secret-sharing'
AUTHOR = 'Franz Geffke'
AUTHOR_EMAIL = 'franz@pantherx.org'
URL = 'https://git.pantherx.org/development/applications/px-secret-sharing'

LICENSE = 'MIT'
DESCRIPTION = 'Split a secret to, or recover from a partial number of pieces.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ['appdirs>=1.4.1,<1.5']

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['px-secret-sharing=px_secret_sharing.command_line:main'],
    },
    packages=find_packages(),
    zip_safe=False
)
