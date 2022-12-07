from IPython import get_ipython
_ip = get_ipython()

import glob
import os
from os import path

ndp_loaded = False

def in_sub_folder(path):
    path = path.split('/')
    for folder in ['inputs', 'models', 'outputs', 'utils']:
        if folder in path:
            return True
    return False

def get_root(path):
    if in_sub_folder(path) is False:
        return path
    else:
        return get_root('/'.join(path.split('/')[:-1]))
    
ROOT_PATH = get_root(os.getcwd())
UTILS_PATH = path.join(ROOT_PATH, "utils")


utils_files = sorted(glob.glob(f"{UTILS_PATH}/*.ipynb"))
for file in utils_files:
    if not file.endswith("__utils__.ipynb"):
        _ip.run_line_magic('run', file)
