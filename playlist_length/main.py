
# -*- coding: utf-8 -*-

import argparse
import multiprocessing
import os
import subprocess as sp
import sys
import re
from concurrent.futures import ProcessPoolExecutor

import magic
from huepy import bold, green, red
from tqdm import tqdm

from playlist_length.utils import pluralize, CacheUtil
from playlist_length.__version__ import __version__


REGEX_MAP = {
    'video': re.compile(r'video|Video'),
    'audio': re.compile(r'audio|Audio'),
    'audio/video': re.compile(r'audio|video|Audio|Video'),
}


def store_in_cache(queue, cache):
    while True:
        result = queue.get()
        if result is None:
            break
        file_hash, value = result
        cache.cache[file_hash] = value
    cache.save()


def duration(args):
    """
    Return the duration of the the file in minutes.
    """
    file_path, queue, cache = args
    file_name = os.path.basename(file_path)
    file_hash = CacheUtil.get_hash(file_name)

    if file_hash in cache:
        return cache[file_hash]

    if not is_media_file(file_path):
        length = 0
    else:
        command = [
            'ffprobe',
            '-loglevel',
            'quiet',
            '-show_entries',
            'format=duration',
            '-print_format',
            'default=nokey=1:noprint_wrappers=1',
            '-i',
            file_path
        ]
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
        result, error = pipe.communicate()
        length = 0 if not result else float(result) / 60
    queue.put((file_hash, length))
    return length


def is_media_file(file_path):
    try:
        match_object = media_type.match(magic.from_file(file_path, mime=True))  # noqa
    except IOError:
        # Probably this directory contains some file/folder that the
        # user don't have permission to read or maybe it is a symlinked
        # file.
        media_file = False
    else:
        media_file = bool(match_object)
    return media_file


def get_all_files(BASE_PATH, no_subdir):

    def with_subdir():
        return (
            os.path.join(root, file)