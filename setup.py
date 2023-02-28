
from setuptools import setup

from playlist_length.__version__ import __version__


requires = (
    'huepy==0.9.6',
    'python-magic>=0.4.15',
    'tqdm>=4.19.9',
    'futures;python_version<"3.4"',
)

setup(
    name='playlist-length',
    version=__version__,
    description='A command-line tool to get length of all audios/videos in a directory',
    long_description=open('README.md').read().strip(),