
import hashlib
import os
import pickle


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.playlist_length')
os.makedirs(CACHE_DIR, exist_ok=True)
