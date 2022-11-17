
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