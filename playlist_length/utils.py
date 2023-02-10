
import hashlib
import os
import pickle


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.playlist_length')
os.makedirs(CACHE_DIR, exist_ok=True)


def pluralize(number, base, suffix):
    if number < 2:
        return '{} {}'.format(number, base)
    return '{} {}{}'.format(number, base, suffix)


class CacheUtil:
    def __init__(self, path, media_type):