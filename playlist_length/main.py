
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
